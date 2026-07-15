from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    sender: str | None = None
    recipients: Sequence[str] | None = None
    subject: str | None = None
    body: str | None = None
    html: str | None = None
    attachments: Sequence[Any] | None = None
    metadata: Mapping[str, Any] | None = None
