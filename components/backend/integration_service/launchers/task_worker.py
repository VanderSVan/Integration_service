import logging
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from integration_service.adapters import (
    api,
    database,
    email_standardization,
    phone_validation,
    gpt_generation,
    message_bus,
    log
)
from integration_service.adapters.email_standardization import DadataEmailStandardizer
from integration_service.adapters.gpt_generation import YandexGPTGenerator
from integration_service.adapters.message_bus import consumers
from integration_service.adapters.phone_validation import DadataPhoneValidator
from integration_service.application import use_cases


class Settings:
    api = api.Settings()
    db = database.Settings()
    dadata_phone_service = phone_validation.dadata_service.Settings()
    dadata_email_service = email_standardization.dadata_service.Settings()
    yandex_gpt_service = gpt_generation.yandex_service.Settings()
    message_bus = message_bus.Settings()


class Logger:
    worker = logging.getLogger(message_bus.LOGGER_PREFIX)
    log.configure(Settings.db.LOGGING_CONFIG, Settings.message_bus.LOGGING_CONFIG)


class DB:
    async_engine = create_async_engine(Settings.db.DATABASE_URL, future=True)

    context = database.AsyncTransactionContext(bind=async_engine, expire_on_commit=False)

    tasks_repo = database.repositories.TasksRepo(context=context)


class Application:
    task_handler = use_cases.TaskHandler(
        phone_validator=DadataPhoneValidator(
            api_url=Settings.dadata_phone_service.API_URL,
            api_key=Settings.dadata_phone_service.API_KEY,
            secret_key=Settings.dadata_phone_service.SECRET_KEY
        ),
        email_validator=DadataEmailStandardizer(
            api_url=Settings.dadata_email_service.API_URL,
            api_key=Settings.dadata_email_service.API_KEY,
            secret_key=Settings.dadata_email_service.SECRET_KEY
        ),
        gpt_generator=YandexGPTGenerator(
            api_url=Settings.yandex_gpt_service.API_URL,
            api_key=Settings.yandex_gpt_service.IAM_TOKEN,
            folder_id=Settings.yandex_gpt_service.FOLDER_ID
        ),
        tasks_repo=DB.tasks_repo
    )


class MessageBus:
    consumer_queue = 'TaskProcessingQueue'
    consumer_exchange = 'TaskProcessingExchange'

    publisher_queue = 'TaskResultDeliveryQueue'
    publisher_exchange = 'TaskResultDeliveryExchange'

    retry_worker = message_bus.consumers.RetryConsumer(
        amqp_url=Settings.message_bus.RABBITMQ_URL,
        queue_name=consumer_queue,
        exchange_name=consumer_exchange,
        function=Application.task_handler.execute,
        max_length=10
    )
    publisher = message_bus.Publisher(
        amqp_url=Settings.message_bus.RABBITMQ_URL,
        exchange_name=publisher_exchange,
        queue_name=publisher_queue,
        max_length=1000
    )
    Application.task_handler.publisher = publisher
    Application.task_handler.targets = {'tasks_handler': publisher_queue}


async def main():
    try:
        await asyncio.gather(MessageBus.retry_worker.start())

        # Не прерывать выполнение, чтобы консьюмер продолжал работу
        await asyncio.Event().wait()

    except Exception as e:
        Logger.worker.exception(f"An error occurred: {e}")

    finally:
        await MessageBus.retry_worker.connection.close()


if __name__ == '__main__':
    asyncio.run(main())
