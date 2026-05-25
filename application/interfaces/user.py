import abc

from application.dto.user import CreateUserDTO
from domain.entities.user import UserDM


class IUserReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_username(self, username: str) -> UserDM | None:
        """Returns user by username."""


class IUserSaver(abc.ABC):
    @abc.abstractmethod
    async def create(self, user: CreateUserDTO) -> None:
        """Create new user."""
