from src.core.shared_kernel.application.exceptions.base import BaseFitNearError


class BaseAuthError(BaseFitNearError):
    """Base auth error."""


class AuthorizationError(BaseAuthError):
    """Authorization error."""
