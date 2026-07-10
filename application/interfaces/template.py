import abc


class IHTMLTemplate(abc.ABC):
    @abc.abstractmethod
    async def generate(self, **kwargs: str | int) -> str:
        """Generate templates like HTML etc."""
