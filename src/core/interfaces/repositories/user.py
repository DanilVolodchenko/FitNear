import abc

from src.core.domain.entities.user import UserDM
from src.core.dto.user import CreateUserDTO


class IUserReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, ident: int) -> UserDM | None:
        """Returns user by id."""

    @abc.abstractmethod
    async def get_by_email(self, email: str) -> UserDM | None:
        """Returns user by email."""


class IUserSaver(abc.ABC):
    @abc.abstractmethod
    async def create(self, user: CreateUserDTO) -> UserDM:
        """Create new user."""


class IUserEditor(abc.ABC):
    @abc.abstractmethod
    async def confirm_user_email(self, user_id: int) -> None:
        """Confirm user email."""


class IUserRemover(abc.ABC):
    @abc.abstractmethod
    async def remove_by_email(self, email: str) -> None:
        """Remove user by email."""
