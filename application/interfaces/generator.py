import abc


class IStringGenerator(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, bytes_count: int) -> str:
        """Generage string."""
