from pydantic import Field

from integration_service.application.entities import TaskTypeEnum
from .base import DTO


class Task(DTO):
    task_id: int = Field(ge=1)
    task_type: TaskTypeEnum
    data: str


class TaskResult(DTO):
    id: int | None
    data: dict | list[dict]
    task_type: TaskTypeEnum

    class Config:
        orm_mode = True


class TaskInfo(DTO):
    task_id: int = Field(ge=1)
    id: int = Field(ge=1)
