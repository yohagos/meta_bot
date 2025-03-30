import asyncio, signal, sys
from uuid import uuid4, UUID
from typing import List
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import load_settings
from models.coins import Coin
from models.coins_interest import CoinInterest
from models.coins_history import CoinHistory
from models.transactions import Transaction
from models.enums import TransactionTypeEnum
from models.rabbitmq_config import RabbitMQConfig
from database.db import AsyncSessionLocal
from services.coin_api import coin_api_polling_task
from services.websocket_manager import WebSocketManager
from services.transaction_bot import transaction_bot, transactions_task
from rabbitmq.connection import RabbitMQConnectionManager
from rabbitmq.consumer import consumer, consumer_callback_with_queue
from rabbitmq.aggregatory import aggregator

from utils import logger

settings = load_settings()

_coin_id_1 = uuid4()
_coin_id_2 = uuid4()
_coin_id_3 = uuid4()
_coin_id_4 = uuid4()
_coin_id_5 = uuid4()
_coin_id_6 = uuid4()

_tx_id_1 = uuid4()
_tx_id_2 = uuid4()
_tx_id_3 = uuid4()
_tx_id_4 = uuid4()
_tx_id_5 = uuid4()
_tx_id_6 = uuid4()

_kc_user_1 = UUID('c9c6f233-2116-401b-b372-a7f05c2035a3')
_kc_user_2 = UUID('07c7d7d2-e41d-4214-bccd-0e4c873b0c55')

RABBITMQ_CONFIGS: List[RabbitMQConfig] = [
    RabbitMQConfig(
        id="transactions",
        exchange_name=settings.MQ_TRANSACTION_EXCHANGE,
        exchange_type='direct',
        queue_name=settings.MQ_TRANSACTION_QUEUE,
        routing_key=settings.MQ_TRANSACTION_ROUTING_KEY,
        durable=True,
        auto_delete=False,
        arguments={
            "x-max-length": 10000,
            "x-message-ttl": 300000
        }
    ),
    RabbitMQConfig(
        id="coins",
        exchange_name=settings.MQ_DATA_EXCHANGE,
        exchange_type='direct',
        queue_name=settings.MQ_DATA_QUEUE,
        routing_key=settings.MQ_DATA_ROUTING_KEY,
        durable=True,
        auto_delete=False,
        arguments={
            "x-max-length": 10000,
            "x-message-ttl": 300000
        }
    ),
    RabbitMQConfig(
        id="all",
        exchange_name=settings.MQ_AGGREGATE_EXCHANGE,
        exchange_type='direct',
        queue_name=settings.MQ_AGGREGATE_QUEUE,
        routing_key=settings.MQ_AGGREGATE_ROUTING_KEY,
        durable=True,
        auto_delete=False,
        arguments={
            "x-max-length": 10000,
            "x-message-ttl": 300000
        }
    )
]

COIN_BASE_TEST_DATA: List[Coin] = [
    Coin(
        id=_coin_id_1,
        coin_name='Bitcoin',
        coin_symbol='BTC', 
    ),
    Coin(
        id=_coin_id_2,
        coin_name='Etherum',
        coin_symbol='ETH',
    ),
    Coin(
        id=_coin_id_3,
        coin_name='XRP',
        coin_symbol='XRP', 
    ),
    Coin(
        id=_coin_id_4,
        coin_name='Doge',
        coin_symbol='DGE',
    ),
    Coin(
        id=_coin_id_5,
        coin_name='Test',
        coin_symbol='TST', 
    ),
    Coin(
        id=_coin_id_6,
        coin_name='Elaines',
        coin_symbol='ELA',
    ),
]

COIN_INTEREST_TEST_DATA: List[CoinInterest] = [
    CoinInterest(
        coin_id=_coin_id_1,
        keycloak_user_id=_kc_user_2,
        id=uuid4(),
    ),
    CoinInterest(
        coin_id=_coin_id_2,
        keycloak_user_id=_kc_user_1,
        id=uuid4(),
    ),
    CoinInterest(
        coin_id=_coin_id_3,
        keycloak_user_id=_kc_user_2,
        id=uuid4(),
    ),
    CoinInterest(
        coin_id=_coin_id_4,
        keycloak_user_id=_kc_user_1,
        id=uuid4(),
    )
]

COIN_HISTORY_TEST_DATA: List[CoinHistory] = [
    CoinHistory(
        coin_id=_coin_id_1,
        price=1500.0,
        volume=7,
        market_cap=0.95,
        transaction_id=_tx_id_1,
        id=uuid4(),
    ),
    CoinHistory(
        coin_id=_coin_id_2,
        price=2500.0,
        volume=4,
        market_cap=0.95,
        transaction_id=_tx_id_2,
        id=uuid4(),
    ),
    CoinHistory(
        coin_id=_coin_id_3,
        price=100.0,
        volume=70,
        market_cap=0.65,
        transaction_id=_tx_id_3,
        id=uuid4(),
    ),
    CoinHistory(
        coin_id=_coin_id_4,
        price=250.0,
        volume=400,
        market_cap=0.75,
        transaction_id=_tx_id_4,
        id=uuid4(),
    ),
]

TRANSACTION_TEST_DATA: List[Transaction] = [
    Transaction(
        id=_tx_id_1,
        keycloak_user_id=_kc_user_2,
        coin_id=_coin_id_1,
        amount=5.0,
        price=16000.0,
        transaction_type=TransactionTypeEnum.SOLD,
    ),
    Transaction(
        id=_tx_id_2,
        keycloak_user_id=_kc_user_1,
        coin_id=_coin_id_2,
        amount=3.0,
        price=4000.0,
        transaction_type=TransactionTypeEnum.SOLD,
    ),
    Transaction(
        id=_tx_id_3,
        keycloak_user_id=_kc_user_2,
        coin_id=_coin_id_3,
        amount=50.0,
        price=160000.0,
        transaction_type=TransactionTypeEnum.BOUGHT,
    ),
    Transaction(
        id=_tx_id_4,
        keycloak_user_id=_kc_user_1,
        coin_id=_coin_id_4,
        amount=13.0,
        price=400.0,
        transaction_type=TransactionTypeEnum.BOUGHT,
    ),
    Transaction(
        id=_tx_id_5,
        keycloak_user_id=_kc_user_2,
        coin_id=_coin_id_3,
        amount=5.0,
        price=1000.0,
        transaction_type=TransactionTypeEnum.BOUGHT,
    ),
    Transaction(
        id=_tx_id_6,
        keycloak_user_id=_kc_user_1,
        coin_id=_coin_id_4,
        amount=3.0,
        price=90.0,
        transaction_type=TransactionTypeEnum.BOUGHT,
    ),
]

async def create_test_data(session: AsyncSession):
    existing_coins = await session.exec(select(Coin))
    existing_interests = await session.exec(select(CoinInterest))
    existing_histories = await session.exec(select(CoinHistory))
    existing_mq_configs = await session.exec(select(RabbitMQConfig))

    if existing_coins.first() is None:
        coins = [coin for coin in COIN_BASE_TEST_DATA]
        session.add_all(coins)
    
    if existing_interests.first() is None:
        coins = [coin for coin in COIN_INTEREST_TEST_DATA]
        session.add_all(coins)

    """ if existing_histories.first() is None:
        coins = [coin for coin in COIN_HISTORY_TEST_DATA]
        session.add_all(coins) """

    if existing_mq_configs.first() is None:
        confs = [conf for conf in RABBITMQ_CONFIGS]
        session.add_all(confs)

    await session.commit()



@asynccontextmanager
async def lifespan(app: FastAPI):
    mq_configs = []
    if settings.MODE == 'dev':
        async with AsyncSessionLocal() as session:
            await create_test_data(session)

            result = await session.exec(select(RabbitMQConfig))
            mq_configs = result.all()

    mq_manager = RabbitMQConnectionManager()
    app.state.mq_manager = mq_manager
    app.state.ws_manager = WebSocketManager()
    shared_queue: asyncio.Queue = asyncio.Queue()
    app.state.shared_queue = shared_queue
    tasks = []
    stop_event = asyncio.Event()

    try:
        await mq_manager.get_connection()
        tasks.append(asyncio.create_task(coin_api_polling_task(app, stop_event)))
        if mq_configs:
            for conf in mq_configs:
                tasks.append(
                    asyncio.create_task(
                        consumer(
                            mq_manager, 
                            conf, 
                            consumer_callback_with_queue(app, conf)
                        )
                    )
                )
        
        tasks.append(asyncio.create_task(transaction_bot(stop_event)))
        tasks.append(asyncio.create_task(transactions_task(app, stop_event)))
        tasks.append(asyncio.create_task(aggregator(app, shared_queue, stop_event)))
        yield
    
    finally:
        stop_event.set()
        for task in tasks:
            if task and not task.done():
                task.cancel()
            
                try:
                    await task
                except asyncio.CancelledError:
                    logger.info("Background task canceled : CanceledError")
                except KeyboardInterrupt:
                    logger.info("Background task canceled : KeyboardInterrupt")
                except Exception as e:
                    logger.error(f"Error during task cancelation : {str(e)}")
        await mq_manager.close()
        del app.state.mq_manager
        del app.state.ws_manager
        del app.state.shared_queue

    