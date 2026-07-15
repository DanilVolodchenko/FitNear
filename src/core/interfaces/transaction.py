import abc


class ITransactionManager(abc.ABC):
    @abc.abstractmethod
    async def commit(self) -> None:
        """Commit session."""
