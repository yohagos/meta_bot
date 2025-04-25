import asyncio, aiohttp, json, aio_pika
from typing import Dict, Any, List
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from datetime import datetime
from fastapi import FastAPI

from database import AsyncSessionLocal
from models.coin_stats import Stats
from models.rabbitmq_config import RabbitMQConfig
from rabbitmq import publish_message, RabbitMQConnectionManager


from configs import load_settings
from utils import logger

_settings = load_settings()

COIN_URL = _settings.COIN_URL


async def fetch_coin_data() -> Dict[str, Any]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(COIN_URL) as response:
                response.raise_for_status()
                data = await response.json()
                return {
                    "data": data['data'],
                    "timestamp": data['timestamp']
                }
    except aiohttp.ClientError as e:
        logger.error(f"Coin API request failed")
    except KeyError as e:
        logger.error(f"Invalid Coin API response")
    
    return None

async def load_exchange_info(session: AsyncSession) -> RabbitMQConfig:
    coin_config = await session.get(RabbitMQConfig, "coins")
    return coin_config


async def clear_stats_data(session: AsyncSession):
    if await session.exec(select(Stats)):
        await session.exec(delete(Stats))
        await session.commit()

async def publish_last_message(mq_manager: RabbitMQConnectionManager, config: RabbitMQConfig):
    async with AsyncSessionLocal() as session:
        last_data: List[Stats] = await session.exec(select(Stats))
        payload = json.dumps(
            [item.model_dump() for item in last_data],
            default=str
        ).encode()
        await publish_message(
            mq_manager,
            config,
            payload
        )



async def coin_api_polling_task(app: FastAPI, stop_event: asyncio.Event):
    async with AsyncSessionLocal() as session:
        config = await load_exchange_info(session)
        last_data: List[Stats] = await session.exec(select(Stats))
        

    mq_manager = app.state.mq_manager

    if last_data and mq_manager and config:
        last_payload = json.dumps(
            [item.model_dump() for item in last_data],
            default=str
        ).encode()
        await publish_message(
            mq_manager,
            config,
            last_payload
        )

    while not stop_event.is_set():
        try: 
            start_time = asyncio.get_event_loop().time()
            await mq_manager.get_connection()
            
            async with AsyncSessionLocal() as session:
                data = await fetch_coin_data()
                if not data or "data" not in data:
                    await publish_last_message(mq_manager, config)
                    await asyncio.sleep(20)
                    continue

                coin_data: List[Any] = data['data']
                await clear_stats_data(session)
                timestamp = datetime.fromtimestamp(int(data['timestamp']) / 1e3)

                publishing_data: List[Stats] = []
                for a in coin_data:
                    try:
                        coin = Stats(
                            id=uuid4(),
                            data_id=a['id'],
                            name=a['name'],
                            symbol=a['symbol'],
                            rank=a['rank'],
                            supply=float(a['supply']) if a['supply'] is not None else None,
                            maxSupply=float(a['maxSupply']) if a['maxSupply'] is not None else None,
                            marketCapUsd=float(a['marketCapUsd']) if a['marketCapUsd'] is not None else None,
                            volumeUsd24Hr=float(a['volumeUsd24Hr']) if a['volumeUsd24Hr'] is not None else None,
                            priceUsd=float(a['priceUsd']) if a['priceUsd'] is not None else None,
                            changePercent24Hr=float(a['changePercent24Hr']) if a['changePercent24Hr'] is not None else None,
                            vwap24Hr=float(a['vwap24Hr']) if a['vwap24Hr'] is not None else None,
                            explorer=a['explorer'] if a['explorer'] is not None else None,
                            timestamp=timestamp
                        )
                        
                        session.add(coin)
                        publishing_data.append(coin)

                    except (KeyError, ValueError, TypeError) as e:
                        logger.info(f"error for coin {a.get('id', 'unknown')}: {str(e)}")
                    await asyncio.sleep(0)
                
                await session.commit()
                
                payload = json.dumps(
                    [item.model_dump() for item in publishing_data], 
                    default=str
                ).encode()
                
                await publish_message(
                    manager=mq_manager,
                    config=config,
                    message_body=payload
                )

            elapsed = asyncio.get_event_loop().time() - start_time
            sleep_time = max(0, 20 - elapsed)
            while sleep_time > 0 and not stop_event.is_set():
                await asyncio.sleep(min(1, sleep_time))
                sleep_time -= 1
                
        except (asyncio.CancelledError, KeyboardInterrupt) as e:
            stop_event.set()
            break
        except (aio_pika.exceptions.AMQPConnectionError, aio_pika.exceptions.AMQPError) as e:
            logger.warning(f"RabbitMQ connection error: {str(e)}. Retrying in 2 seconds.")
            await asyncio.sleep(1)
        except SQLAlchemyError as se:
            logger.error(f"Database error: {str(se)}")
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Polling error: {str(e)}", exc_info=True)
            await asyncio.sleep(1)
        