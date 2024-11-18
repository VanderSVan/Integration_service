import json
import logging

from aio_pika import connect_robust, ExchangeType, Message

from integration_service.application import interfaces
from .constants import LOGGER_PREFIX

logger = logging.getLogger(LOGGER_PREFIX)


class Publisher(interfaces.Publisher):
    def __init__(self,
                 amqp_url: str,
                 exchange_name: str,
                 queue_name: str,
                 max_length: int | None
                 ) -> None:
        self.amqp_url = amqp_url
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.max_length = max_length
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        # Подключение к брокеру сообщений и создание канала
        self.connection = await connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()

        # Объявление exchange
        self.exchange = await self.channel.declare_exchange(
            self.exchange_name, ExchangeType.DIRECT, durable=True
        )

        # Объявление и связывание очереди
        await self.declare_queue()

    async def declare_queue(self):
        self.queue = await self.channel.declare_queue(
            self.queue_name,
            durable=True,
            arguments={'x-max-length': self.max_length} if self.max_length else None
        )
        await self.queue.bind(self.exchange, routing_key=self.queue_name)

    async def publish(self, routing_key: str, message_body: dict):
        if self.exchange is None:
            raise RuntimeError("Publisher is not connected to any exchange")

        # Преобразование словаря в JSON-строку
        message = Message(
            body=json.dumps(message_body).encode(),
            content_type='application/json'
        )

        # Публикация сообщения в exchange с заданным routing_key
        await self.exchange.publish(message, routing_key=routing_key)
        logger.info(f"Published message to {routing_key}: {message_body}")

    async def close(self):
        # Закрытие соединения с брокером сообщений
        if self.connection:
            await self.connection.close()
            logger.info("Connection closed")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
