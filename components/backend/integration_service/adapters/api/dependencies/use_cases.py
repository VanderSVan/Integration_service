from abc import ABC, abstractmethod

from integration_service.application import use_cases


class TaskHandler(ABC):
    """
    Необходим для сборки маршрутов (routers).
    Должен быть переопределен на этапе запуска приложения.
    """

    @abstractmethod
    async def execute(self, task):
        ...


async def get_task_handler() -> use_cases.TaskHandler:
    return TaskHandler()
