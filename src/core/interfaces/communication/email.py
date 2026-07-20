import abc
from collections.abc import Sequence
from typing import Any


class IEmailSender(abc.ABC):
    @abc.abstractmethod
    async def send_text(
        self, subject: str, sender: str, recipients: str | Sequence[str], content: str, **kwargs: Any,
    ) -> None:
        """Send message."""
