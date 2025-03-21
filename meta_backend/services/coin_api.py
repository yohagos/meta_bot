import asyncio, aiohttp
from typing import Dict, Any, List
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from datetime import datetime

from database import AsyncSessionLocal
from models import Stats
from rabbitmq import publish_coin_data, rabbitmq_channel_pool
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
    except aiohttp.ClientError() as e:
        logger.error(f"Coin API request failed")
    except KeyError as e:
        logger.error(f"Invalid Coin API response")
    
    return None


async def clear_stats_data(session: AsyncSession):
    if await session.exec(select(Stats)):
        await session.exec(delete(Stats))
        await session.commit()


async def coin_api_polling_task(session: AsyncSession):
    while True:
        start_time = asyncio.get_event_loop().time()
        try: 
            async with AsyncSessionLocal() as session, rabbitmq_channel_pool() as (connection, channel):
                data = await fetch_coin_data()
                if not data or "data" not in data:
                    logger.warning("No data or invalid structure received.")
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
                
                try:
                    await session.commit()
                    await publish_coin_data(channel, publishing_data)
                except SQLAlchemyError as se:
                    await session.rollback()
                    logger.error(f"Commit failed: {str(se)}")
        
        except Exception as e:
            logger.error(f"Critical error : {str(e)}", exc_info=True)

        elapsed = asyncio.get_event_loop().time() - start_time
        sleep_time = max(0, 20 - elapsed)
        await asyncio.sleep(sleep_time)
        