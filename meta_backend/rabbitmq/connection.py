import aio_pika, os
from urllib import parse

from configs import load_settings

settings = load_settings()


active_websockets = set()

class RabbitMQConnection:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        if not self.connection:
            rabbitmq_url = self._build_rabbitmq_url()
            self.connection = await aio_pika.connect_robust(
                rabbitmq_url,
                timeout=30,
                heartbeat=120
            )
            self.channel = await self.connection.channel()

    def _build_rabbitmq_url(self):
        user = settings.MQ_USER
        password = settings.MQ_PASSWORD
        port = os.getenv("MQ_PORT", "5672")
        host = os.getenv("MQ_HOST", "localhost")
        vhost = parse.quote(os.getenv("MQ_VHOST", "/meta"), safe="")
        url = f"amqp://{user}:{password}@{host}:{port}/{vhost}"
        return url

rabbitmq_connection = RabbitMQConnection()