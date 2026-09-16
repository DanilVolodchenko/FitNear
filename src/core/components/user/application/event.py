import dataclasses
from collections.abc import Sequence

from src.core.shared_kernel.application.interfaces.event_bus import Event


@dataclasses.dataclass
class UserEmailConfirmationEvent(Event):
    subject: str
    sender: str
    recipient: Sequence[str] | str
    content: str
