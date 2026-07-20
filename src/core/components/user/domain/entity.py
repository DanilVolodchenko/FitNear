from dataclasses import dataclass
from datetime import datetime

from src.core.components.user.domain.value_object import RegistrationTokenType


@dataclass(slots=True)
class UserDM:
    id: int
    email: str
    name: str
    password: str
    is_confirmed: bool
    created_at: datetime
    updated_at: datetime | None


@dataclass(slots=True)
class RoleDM:
    name: str
    description: str | None


@dataclass(slots=True)
class PermissionDM:
    name: str
    description: str | None


@dataclass(slots=True)
class RegistrationTokenDM:
    id: int
    user_id: int
    token_hash: str
    type: RegistrationTokenType
    active: bool
    expires_at: datetime
    created_at: datetime
