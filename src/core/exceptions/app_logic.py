class AppError(Exception):
    """Base error for application layer."""


class FoundError(AppError):
    """Data/entity found."""


class NotFoundError(AppError):
    """Data/entity not found."""


class SendEmailError(AppError):
    """Send email error."""


class ConfirmationCodeError(AppError):
    """Confirmation token error."""
