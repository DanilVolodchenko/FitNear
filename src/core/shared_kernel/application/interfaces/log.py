from abc import ABC, abstractmethod
from typing import Any


class ILogger(ABC):
    @abstractmethod
    def trace(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Trace level."""

    @abstractmethod
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Debug level."""

    @abstractmethod
    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Info level."""

    @abstractmethod
    def success(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Success level."""

    @abstractmethod
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Warning level."""

    @abstractmethod
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Exception level."""

    @abstractmethod
    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Error level."""

    @abstractmethod
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Critical level."""
