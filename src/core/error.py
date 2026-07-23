class ApplicationError(Exception):
    """Base error for application layer."""


class FoundError(ApplicationError):
    """Data/etity found."""


class NotFoundError(ApplicationError):
    """Data/entity not found."""


class SendEmailError(ApplicationError):
    """Send email error."""


class ConfirmationCodeError(ApplicationError):
    """Confirmation token error."""
