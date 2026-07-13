import abc


class IStringGenerator(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, length: int) -> str:
        """Generage string with length."""
