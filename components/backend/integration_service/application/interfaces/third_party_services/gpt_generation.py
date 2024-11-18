from abc import ABC, abstractmethod
from typing import Dict, Any


class GPTGenerator(ABC):

    @abstractmethod
    async def generate(self, message: str) -> Dict[str, Any]:
        """
        Асинхронный абстрактный метод для работы с gpt.
        :param message: Текст для обработки gpt
        :return: Сгенерированные данные в виде словаря
        """
        ...
