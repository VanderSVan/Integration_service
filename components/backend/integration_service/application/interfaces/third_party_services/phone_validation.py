from abc import ABC, abstractmethod

from integration_service.application import dtos


class PhoneValidator(ABC):

    @abstractmethod
    async def validate(self, phone: str) -> dtos.TaskInfo:
        """
        Асинхронный абстрактный метод для валидации телефона.
        :param phone: Phone для валидации
        :return: Валидированные данные в виде словаря
        """
        ...
