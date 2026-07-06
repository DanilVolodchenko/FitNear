import abc

from application.dto.token import CreateRegisterTokenDTO
from domain.entities.token import RegistrationTokenDM


class IRegistrationTokenReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_token_hash(self, token_hash: str) -> RegistrationTokenDM | None:
        """Get registration token by token_hash."""


class IRegistrationTokenSaver(abc.ABC):
    @abc.abstractmethod
    async def create(self, token_dto: CreateRegisterTokenDTO) -> RegistrationTokenDM:
        """Create registration token."""


class IRegistrationTokenDeactivator(abc.ABC):
    @abc.abstractmethod
    async def deactivate_by_user(self, user_id: int) -> None:
        """Deactivate all token by user_id."""
