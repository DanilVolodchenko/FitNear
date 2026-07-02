from core.errors import BaseError


class ApplicationError(BaseError):
    """Base error for application layer."""


class FoundError(ApplicationError):
    """Data/etity found."""


class NotFoundError(ApplicationError):
    """Data/entity not found."""
