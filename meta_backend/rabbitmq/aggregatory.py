import json, asyncio
from fastapi import FastAPI
from sqlmodel import select

from database import AsyncSessionLocal
from models.rabbitmq_config import RabbitMQConfig
from utils import logger

async def aggregator(
        app: FastAPI,
        shared_queue: asyncio.Queue,
        stop_event: asyncio.Event
) -> None:
    async with AsyncSessionLocal() as session:
        conf: RabbitMQConfig = ( await session.exec(
                select(RabbitMQConfig).where(RabbitMQConfig.id=='all')
            )).first()
    ws_manager = app.state.ws_manager
    if conf:
        while not stop_event.is_set():
            payload = await shared_queue.get()
            text = json.dumps(payload)
            await ws_manager.broadcast('all', text)