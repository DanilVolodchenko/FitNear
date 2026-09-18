from abc import ABC, abstractmethod
from uuid import UUID


class IStringGenerator(ABC):
    @abstractmethod
    async def __call__(self, length: int) -> str:
        """Generate string with length."""


class IUUIDGenerator(ABC):
    @abstractmethod
    async def __call__(self) -> UUID:
        """Generate uuid."""
