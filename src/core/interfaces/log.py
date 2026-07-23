import abc
from typing import Any


class ILogger(abc.ABC):
    @abc.abstractmethod
    def trace(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Trace level."""

    @abc.abstractmethod
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Debug level."""

    @abc.abstractmethod
    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Info level."""

    @abc.abstractmethod
    def success(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Success level."""

    @abc.abstractmethod
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Warning level."""

    @abc.abstractmethod
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Exception level."""

    @abc.abstractmethod
    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Error level."""

    @abc.abstractmethod
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Critical level."""
