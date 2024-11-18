from collections import namedtuple
from typing import Callable, TypeAlias, TypedDict

from pydantic import BaseModel

from integration_service.application import dtos, entities, errors, interfaces

DTO: TypeAlias = BaseModel


# Это TypeAlias
class PublicationTargets(TypedDict, total=False):
    """
    Названия мест куда необходимо опубликовать сообщение.
    Как правило, это название Exchange в RabbitMQ.
    """
    tasks_handler: str


class TaskHandler:
    def __init__(self,
                 phone_validator: interfaces.PhoneValidator,
                 email_validator: interfaces.EmailStandardizer,
                 gpt_generator: interfaces.GPTGenerator,
                 tasks_repo: interfaces.TasksRepo,
                 publisher: interfaces.Publisher | None = None,
                 targets: PublicationTargets | None = None,
                 ) -> None:
        self.phone_validator = phone_validator
        self.email_validator = email_validator
        self.gpt_generator = gpt_generator
        self.tasks_repo = tasks_repo
        self.publisher = publisher
        self.targets = targets
        self.service_selection_strategy = _TaskProcessingStrategySelector(
            phone_validator=self.phone_validator,
            email_validator=self.email_validator,
            gpt_generator=self.gpt_generator
        )

    async def execute(self, task_id: int, task_type: str, data: str) -> dtos.TaskInfo:
        task: dtos.Task = dtos.Task(task_id=task_id, task_type=task_type, data=data)
        service_method: Callable = self.service_selection_strategy.get_method(task=task)
        service_response: DTO = await service_method(task.data)

        task_result_info: dtos.TaskResult = dtos.TaskResult(
            id=None,
            data=service_response.dict(),
            task_type=task.task_type,
        )
        new_task_result: entities.TaskResult = task_result_info.create_obj(entities.TaskResult)
        saved_task_result: entities.TaskResult = await self.tasks_repo.add(task=new_task_result)
        result: dtos.TaskInfo = dtos.TaskInfo(task_id=task.task_id, id=saved_task_result.id)

        if self.publisher:
            target = self.targets['tasks_handler']
            print(f'Публикую сообщение в очередь {target}')
            if not self.targets or not self.targets.get('tasks_handler'):
                raise errors.TargetNamesError

            async with self.publisher as publisher:
                await publisher.publish(self.targets['tasks_handler'], result.dict())
        return result


class _TaskProcessingStrategySelector:
    def __init__(self,
                 phone_validator: interfaces.PhoneValidator,
                 email_validator: interfaces.EmailStandardizer,
                 gpt_generator: interfaces.GPTGenerator
                 ) -> None:
        self.email_validator = email_validator
        self.phone_validator = phone_validator
        self.gpt_generator = gpt_generator
        self.StrategyKey = namedtuple(
            'StrategyKey',
            [
                entities.TaskTypeEnum.phone.value,
                entities.TaskTypeEnum.email.value,
                entities.TaskTypeEnum.gpt.value
            ]
        )
        self.strategies: dict[namedtuple, Callable] = {
            self.StrategyKey(True, False, False): (
                self.phone_validator.validate
            ),
            self.StrategyKey(False, True, False): (
                self.email_validator.standardize
            ),
            self.StrategyKey(False, False, True): (
                self.gpt_generator.generate
            )
        }

    def _build_key(self, task: dtos.Task) -> namedtuple:
        return self.StrategyKey(
            True if task.task_type == entities.TaskTypeEnum.phone else False,
            True if task.task_type == entities.TaskTypeEnum.email else False,
            True if task.task_type == entities.TaskTypeEnum.gpt else False
        )

    def get_method(self, task: dtos.Task) -> Callable:
        key: namedtuple = self._build_key(task)
        return self.strategies[key]
