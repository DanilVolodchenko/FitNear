from abc import ABC, abstractmethod
from uuid import UUID

from src.core.shared_kernel.domain.entity import AuthTokenDM


class IAuthTokenSaver(ABC):
    @abstractmethod
    async def add(self, auth_token_dm: AuthTokenDM) -> None:
        """Create auth token."""


class IAuthTokenReader(ABC):
    @abstractmethod
    async def get_by_id(self, ident: UUID) -> AuthTokenDM | None:
        """Returns auth token domain model by ident."""


class IAuthTokenEditor(ABC):
    @abstractmethod
    async def deactivate_by_id(self, ident: UUID) -> None:
        """Deactivate token by ident."""
