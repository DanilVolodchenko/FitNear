from src.core.shared_kernel.application.exceptions.base import BaseFitNearError


class BaseSecurityError(BaseFitNearError):
    """Base security error."""


class JWTError(BaseSecurityError):
    """JWT error."""
