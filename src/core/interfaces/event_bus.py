import abc
import dataclasses


@dataclasses.dataclass
class Event:
    """Базовая модель событий."""


class IEventBus(abc.ABC):
    @abc.abstractmethod
    async def publish(self, event: Event) -> None:
        """Публикует события, которые далее обрабатываются."""
