import abc
from collections.abc import Sequence

from src.core.dto.communication import Message


class IMessageSender(abc.ABC):
    @abc.abstractmethod
    async def send_message(self, message: Message) -> None:
        """Send message."""

    @abc.abstractmethod
    async def send_messages(self, messages: Sequence[Message]) -> None:
        """Send chunk of messages."""
