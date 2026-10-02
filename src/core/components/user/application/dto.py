from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.core.components.user.domain.value_object import Language, Theme


@dataclass(frozen=True, slots=True)
class BaseUserDTO:
    email: str


@dataclass(frozen=True, slots=True)
class RegisterUserDTO(BaseUserDTO):
    name: str
    password: str
    settings: RegisterSettingsDTO


@dataclass(frozen=True, slots=True)
class RegisterSettingsDTO:
    language: Language
    theme: Theme


@dataclass(frozen=True, slots=True)
class RegisteredUserDTO:
    registration_id: UUID
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class ConfirmUserDTO:
    confirmation_code: str


@dataclass(frozen=True, slots=True)
class LoginUserDTO(BaseUserDTO):
    password: str
    ip_address: str | None
    user_agent: str | None


@dataclass(frozen=True, slots=True)
class JWTTokenDTO:
    access: str
    refresh: str
