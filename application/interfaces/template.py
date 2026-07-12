import abc
from pathlib import Path


class IHTMLTemplate(abc.ABC):
    @abc.abstractmethod
    async def generate(self, template_path: Path, **kwargs: str | int) -> str:
        """Generate templates like HTML etc."""
