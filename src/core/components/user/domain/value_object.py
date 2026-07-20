from enum import StrEnum


class RegistrationTokenType(StrEnum):
    EMAIL_CONFIRMATION = 'EMAIL_CONFIRMATION'
    PASSWORD_RESET = 'PASSWORD_RESET'  # noqa: S105
