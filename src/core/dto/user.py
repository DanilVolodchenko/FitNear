from dataclasses import dataclass


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
class ConfirmUserDTO:
    confirmation_code: str
