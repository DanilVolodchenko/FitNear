from abc import ABC, abstractmethod
from uuid import UUID


class IStringGenerator(ABC):
    @abstractmethod
    def generate(self, length: int) -> str:
        """Generate string with length."""


class IUUIDGenerator(ABC):
    @abstractmethod
    def generate(self) -> UUID:
        """Generate uuid."""
