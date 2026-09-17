from dataclasses import dataclass
from datetime import datetime

from src.core.components.user.domain.value_object import LanguageType, RegistrationTokenType, ThemeType


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
    language: LanguageType
    theme: ThemeType

    user_id: int
