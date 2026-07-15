from dataclasses import dataclass
from datetime import datetime

from src.core.domain.value_objects.token_type import RegistrationTokenType


@dataclass(slots=True)
class RegistrationTokenDM:
    id: int
    user_id: int
    token_hash: str
    type: RegistrationTokenType
    active: bool
    expires_at: datetime
    created_at: datetime
