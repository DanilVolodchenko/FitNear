from dataclasses import dataclass
from datetime import datetime

from src.core.components.user.domain.value_object import Language, RegistrationTokenType, Theme, UserRole


@dataclass(slots=True, frozen=True)
class UserDM:
    id: int
    email: str
    role: UserRole
    name: str
    hashed_password: str
    is_confirmed: bool
    created_at: datetime
    updated_at: datetime | None


@dataclass(slots=True, frozen=True)
class SettingsDM:
    id: int
    language: Language
    theme: Theme

    user_id: int


@dataclass(slots=True, frozen=True)
class RoleDM:
    name: str
    description: str | None


@dataclass(slots=True, frozen=True)
class PermissionDM:
    name: str
    description: str | None


@dataclass(slots=True, frozen=True)
class RegistrationTokenDM:
    id: int
    user_id: int
    token_hash: str
    type: RegistrationTokenType
    is_active: bool
    expires_at: datetime
    created_at: datetime
