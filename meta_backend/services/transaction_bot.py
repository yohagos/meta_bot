import random, asyncio, json
from uuid import UUID
from concurrent.futures import ThreadPoolExecutor
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import desc
from fastapi import HTTPException, status, FastAPI
from typing import List

from configs.dependencies import KeycloakUserService, get_keycloak_admin
from database import SessionLocal, AsyncSessionLocal
from models.coins import CoinRead, Coin
from models.rabbitmq_config import RabbitMQConfig
from models.transactions import Transaction, TransactionRead
from models.enums import TransactionTypeEnum
from models.user import User
from rabbitmq.publisher import publish_message
from utils import logger

_COIN_IDS = [
    UUID("e2393a58-ebe6-48cd-afbf-920b50a33944"),  # Bitcoin
    UUID("368e6b10-16d9-43e5-8cc0-eff89f3106c7"),  # Etherum
    UUID("0e356461-6c7e-4ae5-bea0-c83b7f3f2506")   # XRP
]

kc_admin = get_keycloak_admin()
kc_service = KeycloakUserService(kc_admin)

def save_transactions_sync(transaction):
    with SessionLocal() as session:
        session.add(transaction)
        session.commit()
        session.close()

async def transaction_bot(
    stop_event: asyncio.Event
) -> None:
    executor = ThreadPoolExecutor(max_workers=4)
    while not stop_event.is_set():
        try:
            c_id = random.choice(_COIN_IDS)
            tx_type = random.choice([TransactionTypeEnum.SOLD, TransactionTypeEnum.BOUGHT])
            prc = random.uniform(1000, 5000)
            amnt = random.randint(5, 20)

            kc_id = UUID('c9c6f233-2116-401b-b372-a7f05c2035a3')

            new_tx = Transaction(
                keycloak_user_id=kc_id,
                coin_id=c_id,
                transaction_type=tx_type,
                price=round(prc, 2),
                amount=amnt
            )

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(executor, save_transactions_sync, new_tx)
            
            await asyncio.sleep(30)
        
        except Exception as e:
            logger.error(f"Transaction Bot Error : {str(e)}")
            stop_event.set()
            break

async def load_config(session: AsyncSession) -> RabbitMQConfig:
    return await session.get(RabbitMQConfig, 'transactions')

async def _find_coin(coin_id: UUID, session: AsyncSession) -> CoinRead:
    coin: Coin = (await session.exec(select(Coin).where(Coin.id == coin_id))).first()
    return CoinRead.model_validate(coin)

async def _find_user(user_id: UUID) -> User:
    user = kc_service.get_user_info(user_id)
    return User.model_validate(user)

        
async def transactions_task(
        app: FastAPI,
        stop_event: asyncio.Event
):
    async with AsyncSessionLocal() as session:
        conf: RabbitMQConfig = await load_config(session)
        last_data: List[Transaction] = (await session.exec(
            select(Transaction).order_by(desc(Transaction.timestamp)).limit(limit=20)
        )).all()
        body = [
            TransactionRead.model_validate(
                tr,
                update={
                    'coin': await _find_coin(tr.coin_id, session),
                    'user': await _find_user(tr.keycloak_user_id)
                }
            ) for tr in last_data
        ]
    
    mq_manager = app.state.mq_manager

    if body and mq_manager and conf:
        payload = json.dumps(
            [item.model_dump() for item in body],
            default=str
        ).encode()

        await publish_message(
            mq_manager,
            conf,
            payload
        )

    while not stop_event.is_set():
        try:
            async with AsyncSessionLocal() as session:
                data: List[Transaction] = (await session.exec(
                    select(Transaction).order_by(desc(Transaction.timestamp)).limit(limit=20)
                )).all()
                body = [
                    TransactionRead.model_validate(
                        tr,
                        update={
                            'coin': await _find_coin(tr.coin_id, session),
                            'user': await _find_user(tr.keycloak_user_id)
                        }
                    ) for tr in data
                ]
                payload = json.dumps(
                    [item.model_dump() for item in body],
                    default=str
                ).encode()

                await publish_message(
                    mq_manager,
                    conf,
                    payload
                )

            await asyncio.sleep(30)

        except Exception as e:
            logger.error(f"Exception in transaction task : {str(e)}")
            stop_event.set()
            break

            