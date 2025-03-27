import aio_pika
from aio_pika import connect_robust
from aio_pika.abc import AbstractChannel, AbstractExchange, ExchangeType
from urllib import parse
from typing import Optional, Dict

from configs import load_settings
from utils import logger

settings = load_settings()


class RabbitMQConnectionManager:
    def __init__(self):
        self._connection: Optional[aio_pika.RobustConnection] = None
        self._exchanges: Dict[str, AbstractExchange] = {}

    async def _connect(self) -> aio_pika.RobustConnection:
        url = self._build_url()
        conn = await connect_robust(
            url=url,
            timeout=30,
            heartbeat=120
        )
        return conn

    def _build_url(self):
        user = settings.MQ_USER
        password = settings.MQ_PASSWORD
        host = settings.MQ_HOST
        port = settings.MQ_PORT
        vhost = parse.quote(settings.MQ_VHOST, safe="")
        return f"amqp://{user}:{password}@{host}:{port}/{vhost}"
    
    async def get_connection(self) -> aio_pika.RobustConnection:
        if self._connection is None or self._connection.is_closed:
            self._connection = await self._connect()
        return self._connection
        
    async def get_channel(self) -> AbstractChannel:
        connection = await self.get_connection()
        channel = await connection.channel()

        return channel
    
    async def get_exchange(
            self, 
            exchange_name: str, 
            exchange_type: str = 'direct',
            durable: bool = True,
            auto_delete: bool = False
    ) -> AbstractExchange:
        if exchange_name in self._exchanges:
            return self._exchanges[exchange_name]
        channel = await self.get_channel()
        ex_type = ExchangeType.DIRECT if exchange_type == "direct" else exchange_type
        try:
            exchange = await channel.declare_exchange(
                name=exchange_name,
                type=ex_type,
                durable=durable,
                auto_delete=auto_delete
            )
            self._exchanges[exchange_name] = exchange
            return exchange
        except Exception as e:
            logger.error(f"Error declaring exchange {exchange_name}: {e}")
            raise
        
    async def close(self):
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        self._connection = None
        self._exchanges.clear()

