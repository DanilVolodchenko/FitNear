from abc import ABC, abstractmethod
from uuid import UUID

from src.core.components.user.domain.entity import ConfirmationCodeDM, SettingsDM, UserDM


class IUserSaver(ABC):
    @abstractmethod
    async def save(self, user_dm: UserDM) -> None:
        """Save new user."""


class IUserReader(ABC):
    @abstractmethod
    async def get_by_id(self, ident: UUID) -> UserDM | None:
        """Returns user by id."""

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDM | None:
        """Returns user by email."""


class IUserEditor(ABC):
    @abstractmethod
    async def confirm_user_email(self, user_id: UUID) -> None:
        """Confirm user email."""


class IUserRemover(ABC):
    @abstractmethod
    async def remove_by_email(self, email: str) -> None:
        """Remove user by email."""


class ISettingsSaver(ABC):
    @abstractmethod
    async def save(self, settings_dm: SettingsDM) -> None:
        """Create user settings."""


class IConfirmationCodeSaver(ABC):
    @abstractmethod
    async def save(self, confirmation_code_dm: ConfirmationCodeDM) -> None:
        """Save confirmation code."""


class IConfirmationCodeReader(ABC):
    @abstractmethod
    async def get_by_token_hash(self, token_hash: str) -> ConfirmationCodeDM | None:
        """Get confirmation code by token_hash."""

    @abstractmethod
    async def get_by_id(self, ident: UUID) -> ConfirmationCodeDM | None:
        """Get confirmation code by id."""


class IConfirmationCodeEditor(ABC):
    @abstractmethod
    async def deactivate(self, ident: UUID) -> None:
        """Deactivate confirmation code."""
