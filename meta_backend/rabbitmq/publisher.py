import aio_pika, json
from contextlib import asynccontextmanager
from typing import List

from configs import load_settings
from models import Stats
from utils import logger
from . import rabbitmq_connection, RabbitMQConnection

settings = load_settings()

rabbitmq_connection = RabbitMQConnection()

@asynccontextmanager
async def rabbitmq_channel_pool():
    connection = None
    try: 
        await rabbitmq_connection.connect()
        connection = rabbitmq_connection.connection
        channel = rabbitmq_connection.channel
        yield connection, channel
    except Exception as e:
        logger.error(f"RabbitMQ connection failed : {str(e)}")
        raise
    finally:
        if connection:
            await connection.close()
            rabbitmq_connection.connection = None
            rabbitmq_connection.channel = None

async def publish_coin_data(
        channel: aio_pika.abc.AbstractChannel,
        data: List[Stats]
):
    try:
        exchange = await channel.get_exchange(settings.MQ_EXCHANGE)

        payload = json.dumps([item.model_dump() for item in data], default=str).encode()
        message = aio_pika.Message(
            body=payload,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await exchange.publish(
            message=message,
            routing_key=settings.MQ_ROUTING_KEY
        )
    except aio_pika.exceptions.AMQPError as ae:
        logger.error(f"RabbitMQ Error : {str(ae)}")
    except aio_pika.exceptions.ChannelInvalidStateError as cie:
        logger.error("Channel closed. Reconnecting..")
        channel = rabbitmq_connection.channel
        await publish_coin_data(channel, data)

