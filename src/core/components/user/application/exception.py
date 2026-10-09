from src.core.shared_kernel.application.exceptions.base import BaseFitNearError


class BaseUserComponentError(BaseFitNearError):
    """Base error for application layer."""


class UserError(BaseUserComponentError):
    """User error."""


class RegistrationTokenError(BaseUserComponentError):
    """Token error."""
