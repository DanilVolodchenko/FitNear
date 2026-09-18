from enum import StrEnum


class UserRole(StrEnum):
    CLIENT = 'client'
    STUFF = 'stuff'
    ADMIN = 'admin'


class RegistrationTokenType(StrEnum):
    EMAIL_CONFIRMATION = 'email_confirmation'
    PASSWORD_RESET = 'password_reset'  # noqa: S105


class AuthTokenType(StrEnum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class Language(StrEnum):
    RU = 'ru'
    EN = 'en'


class Theme(StrEnum):
    WHITE = 'white'
    BLACK = 'black'
