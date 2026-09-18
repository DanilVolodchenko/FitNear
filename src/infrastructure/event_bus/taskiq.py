import dataclasses

from taskiq.decor import AsyncTaskiqDecoratedTask

from src.core.components.user.application.event import UserEmailConfirmationEvent
from src.core.shared_kernel.application.interfaces.event_bus import Event, IEventBus
from src.core.shared_kernel.application.interfaces.log import ILogger
from src.infrastructure.tasks.communication import send_email_task


class TaskiqEventBus(IEventBus):
    def __init__(self, logger: ILogger) -> None:
        self._logger = logger

        self._handlers: dict[type[Event], list[AsyncTaskiqDecoratedTask]] = {
            UserEmailConfirmationEvent: [send_email_task],
        }

    async def publish(self, event: Event) -> None:
        handlers = self._handlers.get(type(event), [])

        if not handlers:
            self._logger.warning('Handler for event={} not found', event)

        for handler in handlers:
            params = dataclasses.asdict(event)

            await handler.kiq(**params)
