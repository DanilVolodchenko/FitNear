from datetime import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class UserDM:
    id: int | None
    email: str
    name: str
    password: str
    is_comfirmed: bool
    created_at: datetime
    updated_at: datetime | None


@dataclass(slots=True)
class RoleDM:
    name: str
    description: str | None


@dataclass(slots=True)
class PermissionDM:
    name: str
    description: str | None
