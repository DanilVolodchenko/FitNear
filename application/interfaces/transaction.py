import abc


class TransactionManager(abc.ABC):
    @abc.abstractmethod
    async def commit(self) -> None:
        """Commit session."""
