from abc import ABC, abstractmethod

from src.core.components.user.application.dto import CreateRegisterTokenDTO, CreateSettingsDTO, CreateUserDTO
from src.core.components.user.domain.entity import RegistrationTokenDM, SettingsDM, UserDM


class IUserSaver(ABC):
    @abstractmethod
    async def create(self, user_dto: CreateUserDTO) -> UserDM:
        """Create new user."""


class IUserReader(ABC):
    @abstractmethod
    async def get_by_id(self, ident: int) -> UserDM | None:
        """Returns user by id."""

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDM | None:
        """Returns user by email."""


class IUserEditor(ABC):
    @abstractmethod
    async def confirm_user_email(self, user_id: int) -> None:
        """Confirm user email."""


class IUserRemover(ABC):
    @abstractmethod
    async def remove_by_email(self, email: str) -> None:
        """Remove user by email."""


class ISettingsSaver(ABC):
    @abstractmethod
    async def create(self, settings_dto: CreateSettingsDTO) -> SettingsDM:
        """Create user settings."""


class IRegistrationTokenSaver(ABC):
    @abstractmethod
    async def create(self, token_dto: CreateRegisterTokenDTO) -> RegistrationTokenDM:
        """Create registration token."""


class IRegistrationTokenReader(ABC):
    @abstractmethod
    async def get_by_token_hash(self, token_hash: str) -> RegistrationTokenDM | None:
        """Get token by token_hash."""

    @abstractmethod
    async def get_by_id(self, ident: int) -> RegistrationTokenDM | None:
        """Get token by id."""


class IRegistrationTokenEditor(ABC):
    @abstractmethod
    async def deactivate(self, token_id: int) -> None:
        """Deactivate token."""
