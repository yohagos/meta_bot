import asyncio, json
from typing import Set, Optional, Callable, Awaitable
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from aio_pika import IncomingMessage, ExchangeType

from configs import load_settings
from utils import logger
from rabbitmq.connection import RabbitMQConnectionManager
from models.rabbitmq_config import RabbitMQConfig
from services.websocket_manager import WebSocketManager


settings = load_settings()

async def consumer(
        manager: RabbitMQConnectionManager,
        config: RabbitMQConfig,
        callback: Callable[[IncomingMessage], Awaitable[None]]
) -> None:
    channel = await manager.get_channel()
    exchange = await manager.get_exchange(
        exchange_name=config.exchange_name,
        exchange_type=config.exchange_type,
        durable=config.durable,
        auto_delete=config.auto_delete
    )

    queue = await channel.declare_queue(
        name=config.queue_name,
        durable=config.durable,
        auto_delete=config.auto_delete,
        arguments=config.arguments
    )

    await queue.bind(
        exchange=exchange,
        routing_key=config.routing_key
    )

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            try:
                await callback(message)
            except Exception as e:
                logger.error(f"Error processing message : {str(e)}")
                continue

async def consumer_callback(
        message: IncomingMessage,
        app: FastAPI,
        conf: RabbitMQConfig
) -> None:
    async with message.process():
        try:
            payload = json.loads(message.body.decode())
            if isinstance(payload, list):
                text = json.dumps(payload)
                await app.state.ws_manager.broadcast(conf.exchange_name, text)
            elif isinstance(payload, dict):
                text = json.dumps(payload)
                await app.state.ws_manager.broadcast(conf.exchange_name, text)
            else:
                raise ValueError("Unexpected payload type")
            
        except Exception as e:
            logger.error(f"Error consumer : {str(e)}")
            
def consumer_callback_with_app(app: FastAPI, conf: RabbitMQConfig):
    async def _callback(message: IncomingMessage) -> None:
        await consumer_callback(message, app, conf)
    return _callback
