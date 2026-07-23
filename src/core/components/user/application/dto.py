from dataclasses import dataclass
from datetime import datetime

from src.core.components.user.domain.value_object import RegistrationTokenType


@dataclass(frozen=True, slots=True)
class GetUserDTO:
    username: str
    password: str


@dataclass(frozen=True, slots=True)
class CreateUserDTO:
    email: str
    name: str
    password: str
    is_confirmed: bool = False


@dataclass(frozen=True, slots=True)
class RegisterUserDTO:
    email: str
    name: str
    password: str


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
    is_active: bool = True
