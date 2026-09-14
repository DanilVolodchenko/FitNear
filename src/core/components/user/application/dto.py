from dataclasses import dataclass
from datetime import datetime

from src.core.components.user.domain.value_object import LanguageType, RegistrationTokenType, ThemeType


@dataclass(frozen=True, slots=True)
class GetUserDTO:
    username: str
    password: str


@dataclass(frozen=True, slots=True)
class CreateUserDTO:
    email: str
    name: str
    hashed_password: str
    is_confirmed: bool = False


@dataclass(frozen=True, slots=True)
class RegisterUserDTO:
    email: str
    name: str
    password: str
    settings: RegisterSettingsDTO


@dataclass(frozen=True, slots=True)
class RegisterSettingsDTO:
    language: LanguageType
    theme: ThemeType


@dataclass(frozen=True, slots=True)
class RegisteredUserDTO:
    registration_id: int
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class ConfirmUserDTO:
    confirmation_code: str


@dataclass(frozen=True, slots=True)
class CreateRegisterTokenDTO:
    user_id: int
    token_hash: str
    type: RegistrationTokenType
    expires_at: datetime
    attempts: int = 1
    is_active: bool = True


@dataclass(frozen=True, slots=True)
class CreateSettingsDTO:
    language: LanguageType
    theme: ThemeType

    user_id: int
