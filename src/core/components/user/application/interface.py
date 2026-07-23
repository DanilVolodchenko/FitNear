import abc

from src.core.components.user.application.dto import CreateRegisterTokenDTO, CreateUserDTO
from src.core.components.user.domain.entity import RegistrationTokenDM, UserDM


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


class IRegistrationTokenReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_token_hash(self, token_hash: str) -> RegistrationTokenDM | None:
        """Get token by token_hash."""

    @abc.abstractmethod
    async def get_by_id(self, ident: int) -> RegistrationTokenDM | None:
        """Get token by id."""


class IRegistrationTokenSaver(abc.ABC):
    @abc.abstractmethod
    async def create(self, token_dto: CreateRegisterTokenDTO) -> RegistrationTokenDM:
        """Create registration token."""


class IRegistrationTokenEditor(abc.ABC):
    @abc.abstractmethod
    async def deactivate(self, token_id: int) -> None:
        """Deactivate token."""
