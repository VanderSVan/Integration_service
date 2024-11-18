from integration_service.application import interfaces, entities
from .base import BaseRepository


class TasksRepo(BaseRepository, interfaces.TasksRepo):
    async def add(self, task: entities.TaskResult) -> entities.TaskResult:
        """Сохраняет задачу в базе данных и возвращает ее"""
        async with self.context as session:
            session.add(task)
            await session.flush()
            await session.refresh(task)
            return task
