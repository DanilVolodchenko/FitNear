import dataclasses

from taskiq.decor import AsyncTaskiqDecoratedTask

from src.core.components.user.application.event import UserEmailConfirmationEvent
from src.core.interfaces.event_bus import Event, IEventBus


class TaskiqEventBus(IEventBus):
    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[AsyncTaskiqDecoratedTask]] = {
            UserEmailConfirmationEvent: [],
        }

    async def publish(self, event: Event) -> None:
        handlers = self._handlers.get(type(event), [])

        for handler in handlers:
            await handler.kiq(dataclasses.asdict(event))
