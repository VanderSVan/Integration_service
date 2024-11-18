from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class Publisher:
    @abstractmethod
    async def publish(self, routing_key: str, message_body: dict):
        ...
