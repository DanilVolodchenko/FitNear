import dataclasses
from abc import ABC, abstractmethod


@dataclasses.dataclass
class Event:
    """Базовая модель событий."""


class IEventBus(ABC):
    @abstractmethod
    async def publish(self, event: Event) -> None:
        """Публикует события, которые далее обрабатываются."""
