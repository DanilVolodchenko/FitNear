from enum import StrEnum


class RegistrationTokenType(StrEnum):
    EMAIL_CONFIRMATION = 'email_confirmation'
    PASSWORD_RESET = 'password_reset'  # noqa: S105


class Language(StrEnum):
    RU = 'ru'
    EN = 'en'


class Theme(StrEnum):
    WHITE = 'white'
    BLACK = 'black'
