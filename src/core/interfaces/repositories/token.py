import abc

from src.core.domain.entities.token import RegistrationTokenDM
from src.core.dto.token import CreateRegisterTokenDTO


class IRegistrationTokenReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_token_hash(self, token_hash: str) -> RegistrationTokenDM | None:
        """Get registration token by token_hash."""


class IRegistrationTokenSaver(abc.ABC):
    @abc.abstractmethod
    async def create(self, token_dto: CreateRegisterTokenDTO) -> RegistrationTokenDM:
        """Create registration token."""
