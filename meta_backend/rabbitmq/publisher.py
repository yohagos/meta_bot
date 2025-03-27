import aio_pika, json, asyncio
from aio_pika import Message, DeliveryMode
from contextlib import asynccontextmanager
from typing import List

from configs import load_settings
from models import Stats
from utils import logger
from .connection import RabbitMQConnectionManager 
from models.rabbitmq_config import RabbitMQConfig

settings = load_settings()

async def publish_message(
        manager: RabbitMQConnectionManager,
        config: RabbitMQConfig,
        message_body: bytes
):
    try:
        await asyncio.sleep(0)
        exchange = await manager.get_exchange(
            exchange_name=config.exchange_name
        )
        message = Message(
            body=message_body,
            delivery_mode=DeliveryMode.PERSISTENT
        )
        await exchange.publish(message=message, routing_key=config.routing_key)
    except aio_pika.exceptions.AMQPError as e:
        logger.error(f"Publish error : {str(e)}")
        raise
