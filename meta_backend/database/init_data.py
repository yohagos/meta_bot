import asyncio
from uuid import uuid4, UUID
from typing import List
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI

from configs import load_settings
from models import Coin, CoinInterest, Transaction, TransactionTypeEnum, CoinHistory
from database import AsyncSessionLocal
from services import coin_api_polling_task
from rabbitmq import start_consumer

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


COIN_BASE_TEST_DATA: List[Coin] = [
    Coin(
        id=_coin_id_1,
        coin_name='Bitcoin',
        coin_symbol='BTC', 
        created_date=datetime.now(timezone.utc)  
    ),
    Coin(
        id=_coin_id_2,
        coin_name='Etherum',
        coin_symbol='ETH',
        created_date=datetime.now(timezone.utc)
    ),
    Coin(
        id=_coin_id_3,
        coin_name='Ripple',
        coin_symbol='XRP', 
        created_date=datetime.now(timezone.utc)  
    ),
    Coin(
        id=_coin_id_4,
        coin_name='Doge',
        coin_symbol='DGE',
        created_date=datetime.now(timezone.utc)
    ),
    Coin(
        id=_coin_id_5,
        coin_name='Test',
        coin_symbol='TST', 
        created_date=datetime.now(timezone.utc)  
    ),
    Coin(
        id=_coin_id_6,
        coin_name='Elaines',
        coin_symbol='ELA',
        created_date=datetime.now(timezone.utc)
    ),
]

COIN_INTEREST_TEST_DATA: List[CoinInterest] = [
    CoinInterest(
        coin_id=_coin_id_1,
        keycloak_user_id=_kc_user_2,
        id=uuid4(),
        created_date=datetime.now(timezone.utc)
    ),
    CoinInterest(
        coin_id=_coin_id_2,
        keycloak_user_id=_kc_user_1,
        id=uuid4(),
        created_date=datetime.now(timezone.utc)
    ),
    CoinInterest(
        coin_id=_coin_id_3,
        keycloak_user_id=_kc_user_2,
        id=uuid4(),
        created_date=datetime.now(timezone.utc)
    ),
    CoinInterest(
        coin_id=_coin_id_4,
        keycloak_user_id=_kc_user_1,
        id=uuid4(),
        created_date=datetime.now(timezone.utc)
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
        timestamp=datetime.now(timezone.utc)
    ),
    CoinHistory(
        coin_id=_coin_id_2,
        price=2500.0,
        volume=4,
        market_cap=0.95,
        transaction_id=_tx_id_2,
        id=uuid4(),
        timestamp=datetime.now(timezone.utc)
    ),
    CoinHistory(
        coin_id=_coin_id_3,
        price=100.0,
        volume=70,
        market_cap=0.65,
        transaction_id=_tx_id_3,
        id=uuid4(),
        timestamp=datetime.now(timezone.utc)
    ),
    CoinHistory(
        coin_id=_coin_id_4,
        price=250.0,
        volume=400,
        market_cap=0.75,
        transaction_id=_tx_id_4,
        id=uuid4(),
        timestamp=datetime.now(timezone.utc)
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
        timestamp=datetime.now(timezone.utc)
    ),
    Transaction(
        id=_tx_id_2,
        keycloak_user_id=_kc_user_1,
        coin_id=_coin_id_2,
        amount=3.0,
        price=4000.0,
        transaction_type=TransactionTypeEnum.SOLD,
        timestamp=datetime.now(timezone.utc)
    ),
    Transaction(
        id=_tx_id_3,
        keycloak_user_id=_kc_user_2,
        coin_id=_coin_id_3,
        amount=50.0,
        price=160000.0,
        transaction_type=TransactionTypeEnum.BOUGHT,
        timestamp=datetime.now(timezone.utc)
    ),
    Transaction(
        id=_tx_id_4,
        keycloak_user_id=_kc_user_1,
        coin_id=_coin_id_4,
        amount=13.0,
        price=400.0,
        transaction_type=TransactionTypeEnum.BOUGHT,
        timestamp=datetime.now(timezone.utc)
    ),
    Transaction(
        id=_tx_id_5,
        keycloak_user_id=_kc_user_2,
        coin_id=_coin_id_3,
        amount=5.0,
        price=1000.0,
        transaction_type=TransactionTypeEnum.BOUGHT,
        timestamp=datetime.now(timezone.utc)
    ),
    Transaction(
        id=_tx_id_6,
        keycloak_user_id=_kc_user_1,
        coin_id=_coin_id_4,
        amount=3.0,
        price=90.0,
        transaction_type=TransactionTypeEnum.BOUGHT,
        timestamp=datetime.now(timezone.utc)
    ),
]


@asynccontextmanager
async def lifespan(app: FastAPI):

    await start_consumer()

    async with AsyncSessionLocal() as session:
        task = asyncio.create_task(coin_api_polling_task(session))
        yield
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    