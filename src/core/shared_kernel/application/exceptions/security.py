class SecurityBaseError(Exception):
    """Base security error."""


class JWTError(SecurityBaseError):
    """JWT error."""
