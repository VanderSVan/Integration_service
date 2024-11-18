import json
import logging
from typing import Callable, Optional

from aio_pika import connect_robust, ExchangeType, IncomingMessage, Message

from .constants import (
    LOGGER_PREFIX,
    DEFAULT_ERROR_MAX_RETRY_ATTEMPTS,
    ERROR_DEAD_EXCHANGE,
    ERROR_DEAD_QUEUE_SUFFIX
)

logger = logging.getLogger(LOGGER_PREFIX)


class BaseConsumer:
    def __init__(self,
                 amqp_url: str,
                 queue_name: str,
                 exchange_name: str,
                 max_length: int | None = None
                 ):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.max_length = max_length
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(self):
        # Подключение к брокеру сообщений и создание канала
        self.connection = await connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()

        # Объявление exchange
        self.exchange = await self.channel.declare_exchange(
            self.exchange_name, ExchangeType.DIRECT, durable=True
        )

        # Определение аргументов очереди
        queue_args = {}
        if self.max_length is not None:
            queue_args['x-max-length'] = self.max_length

        # Объявление очереди
        self.queue = await self.channel.declare_queue(
            self.queue_name, durable=True, arguments=queue_args
        )

        # Привязка очереди к exchange
        await self.queue.bind(self.exchange, routing_key=self.queue_name)

    async def start(self):
        # Запуск потребителя
        await self.connect()
        logger.info(f"Starting consumer for queue: {self.queue_name}")

        # Потребление сообщений с использованием метода on_message
        await self.queue.consume(self.on_message)

    async def on_message(self, message: IncomingMessage):
        # Этот метод должен быть переопределен в наследуемых классах
        raise NotImplementedError("Subclasses should implement this!")


class SimpleConsumer(BaseConsumer):
    def __init__(self, amqp_url: str, queue_name: str, exchange_name: str, function: Callable,
                 max_length: Optional[int] = None):
        super().__init__(amqp_url, queue_name, exchange_name, max_length)
        self.function = function

    async def on_message(self, message: IncomingMessage):
        # Автоматическое подтверждение или отказ в зависимости от результата обработки
        async with message.process():
            try:
                # Декодирование тела сообщения и вызов зарегистрированной функции
                body = message.body.decode()
                logger.info(f"Received message: {body}")
                await self.function(body)
                # Сообщение автоматически подтверждается (ack) при успешном выполнении

            except Exception as e:
                logger.exception(f"Error processing message: {e}")
                # При возникновении ошибки сообщение не подтверждается (nack)
                raise e  # Сообщение будет переотправлено на обработку


class RetryConsumer(BaseConsumer):
    def __init__(self,
                 amqp_url: str,
                 queue_name: str,
                 exchange_name: str,
                 function: Callable,
                 max_length: Optional[int] = None,
                 max_retry_attempts=DEFAULT_ERROR_MAX_RETRY_ATTEMPTS):
        super().__init__(amqp_url, queue_name, exchange_name, max_length)
        self.function = function
        self.max_retry_attempts = max_retry_attempts

    async def on_message(self, message: IncomingMessage):
        async with message.process():
            try:
                body = message.body.decode()
                logger.info(f"Received message: {body}")

                # Преобразование JSON-строки в словарь
                message_data = json.loads(body)
                print(message_data)

                # Вызов функции с распаковкой словаря в аргументы
                await self.function(**message_data)
            except Exception as e:
                logger.exception(f"Error processing message: {e}")

                # Обработка логики ретраев на основе количества попыток
                attempt_count = message.headers.get('x-death', [{}])[0].get('count', 0)
                if attempt_count >= self.max_retry_attempts:
                    logger.error(
                        f"Max retry attempts reached. Moving message to dead letter queue.")
                    await self.move_to_dead_queue(message)
                else:
                    raise e  # Сообщение будет переотправлено для повторной попытки

    async def move_to_dead_queue(self, message: IncomingMessage):
        # Перемещение сообщения в "мертвую" очередь
        dead_exchange = await self.channel.declare_exchange(
            ERROR_DEAD_EXCHANGE, ExchangeType.DIRECT, durable=True
        )
        await dead_exchange.publish(
            Message(body=message.body),
            routing_key=self.queue_name + ERROR_DEAD_QUEUE_SUFFIX
        )
        await message.ack()  # Подтверждаем, что сообщение перемещено
