from dataclasses import dataclass


@dataclass
class GetUserDTO:
    username: str
    password: str


@dataclass
class CreateUserDTO:
    email: str
    name: str
    password: str
    is_confirmed: bool = False
