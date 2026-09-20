from abc import ABC, abstractmethod


class ITransactionManager(ABC):
    @abstractmethod
    async def commit(self) -> None:
        """Commit session."""
