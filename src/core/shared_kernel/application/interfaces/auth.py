from abc import ABC, abstractmethod

from src.core.shared_kernel.application.dto.token import CreateAuthTokenDTO
from src.core.shared_kernel.domain.entity import AuthTokenDM


class IAuthTokenSaver(ABC):
    @abstractmethod
    async def create(self, create_token_dto: CreateAuthTokenDTO) -> AuthTokenDM:
        """Create auth token."""


class IAuthTokenReader(ABC):
    @abstractmethod
    async def get_by_id(self, ident: int) -> AuthTokenDM:
        """Returns auth token domain model."""


class IAuthTokenEditor(ABC):
    @abstractmethod
    async def deactivate_by_id(self, ident: int) -> None:
        """Deactivate token."""
