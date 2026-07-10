import abc

from application.domain.entities.user import UserDM
from application.dto.user import CreateUserDTO


class IUserReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_email(self, email: str) -> UserDM | None:
        """Returns user by email."""


class IUserSaver(abc.ABC):
    @abc.abstractmethod
    async def create(self, user: CreateUserDTO) -> UserDM:
        """Create new user."""


class IUserEmailConfirmer(abc.ABC):
    @abc.abstractmethod
    async def send(self, url: str, title: str, description: str) -> None:
        """Send user info to confirm user email."""
