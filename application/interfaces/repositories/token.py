import abc

from application.domain.entities.token import RegistrationTokenDM
from application.dto.token import CreateRegisterTokenDTO


class IRegistrationTokenReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_token_hash(self, token_hash: str) -> RegistrationTokenDM | None:
        """Get registration token by token_hash."""


class IRegistrationTokenSaver(abc.ABC):
    @abc.abstractmethod
    async def create(self, token_dto: CreateRegisterTokenDTO) -> RegistrationTokenDM:
        """Create registration token."""
