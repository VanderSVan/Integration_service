from dataclasses import dataclass
from enum import Enum


class TaskTypeEnum(str, Enum):
    phone = 'phone'
    email = 'email'
    gpt = 'gpt'


@dataclass(kw_only=True)
class TaskResult:
    id: int | None
    data: dict | list[dict]
    task_type: TaskTypeEnum
