from dataclasses import dataclass


@dataclass(slots=True)
class UserDM:
    id: int | None
    name: str
    username: str
    password: str


@dataclass(slots=True)
class RoleDM:
    name: str
    description: str | None


@dataclass(slots=True)
class PermissionDM:
    name: str
    description: str | None
