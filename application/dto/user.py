from dataclasses import dataclass


@dataclass
class GetUserDTO:
    username: str
    password: str


@dataclass
class CreateUserDTO:
    username: str
    name: str
    password: str
