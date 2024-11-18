from abc import ABC, abstractmethod

from integration_service.application import entities


class TasksRepo(ABC):

    @abstractmethod
    async def add(self, task: entities.TaskResult) -> entities.TaskResult:
        ...
