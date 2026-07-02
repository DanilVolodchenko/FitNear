import abc

from application.dto.user import CreateUserDTO
from domain.entities.user import UserDM


class IUserReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_email(self, email: str) -> UserDM | None:
        """Returns user by email."""


class IUserSaver(abc.ABC):
    @abc.abstractmethod
    async def create(self, user: CreateUserDTO) -> int:
        """Create new user."""
