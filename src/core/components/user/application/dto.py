from dataclasses import dataclass
from datetime import datetime

from src.core.components.user.domain.value_object import Language, RegistrationTokenType, Theme


@dataclass(frozen=True, slots=True)
class BaseUserDTO:
    email: str


@dataclass(frozen=True, slots=True)
class RegisterUserDTO(BaseUserDTO):
    name: str
    password: str
    settings: RegisterSettingsDTO


@dataclass(frozen=True, slots=True)
class CreateUserDTO(BaseUserDTO):
    name: str
    hashed_password: str
    is_confirmed: bool = False


@dataclass(frozen=True, slots=True)
class RegisterSettingsDTO:
    language: Language
    theme: Theme


@dataclass(frozen=True, slots=True)
class RegisteredUserDTO:
    registration_id: int
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class ConfirmUserDTO:
    confirmation_code: str


@dataclass(frozen=True, slots=True)
class LoginUserDTO(BaseUserDTO):
    password: str


@dataclass(frozen=True, slots=True)
class CreateRegisterTokenDTO:
    user_id: int
    token_hash: str
    type: RegistrationTokenType
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class CreateSettingsDTO:
    language: Language
    theme: Theme

    user_id: int


@dataclass(frozen=True, slots=True)
class JWTTokenDTO:
    access: str
    refresh: str
