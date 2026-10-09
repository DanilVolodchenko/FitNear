from abc import ABC, abstractmethod
from uuid import UUID

from src.core.shared_kernel.domain.entity import RefreshTokenDM


class IRefreshTokenSaver(ABC):
    @abstractmethod
    async def add(self, refresh_token_dm: RefreshTokenDM) -> None:
        """Create refresh token."""


class IRefreshTokenReader(ABC):
    @abstractmethod
    async def get_by_id(self, ident: UUID) -> RefreshTokenDM | None:
        """Returns refresh token by ident."""


class IRefreshTokenEditor(ABC):
    @abstractmethod
    async def deactivate_by_id(self, ident: UUID) -> None:
        """Deactivate token by ident."""
