import abc

from src.core.domain.entities.token import RegistrationTokenDM
from src.core.dto.token import CreateRegisterTokenDTO


class IRegistrationTokenReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_token_hash(self, token_hash: str) -> RegistrationTokenDM | None:
        """Get token by token_hash."""

    @abc.abstractmethod
    async def get_by_user_id(self, user_id: int) -> RegistrationTokenDM | None:
        """Get token by user_id."""


class IRegistrationTokenSaver(abc.ABC):
    @abc.abstractmethod
    async def create(self, token_dto: CreateRegisterTokenDTO) -> RegistrationTokenDM:
        """Create registration token."""


class IRegistrationTokenEditor(abc.ABC):
    @abc.abstractmethod
    async def deactivate(self, token_id: int) -> None:
        """Deactivate token."""
