from abc import ABC, abstractmethod
from typing import Dict, Any


class EmailStandardizer(ABC):

    @abstractmethod
    async def standardize(self, email: str) -> Dict[str, Any]:
        """
        Асинхронный абстрактный метод для стандартизации email.
        :param email: Email для стандартизации
        :return: Стандартизованные данные в виде словаря
        """
        ...
