from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = 'admin'
    STUFF = 'stuff'
    CLIENT = 'client'


class RegistrationTokenType(StrEnum):
    EMAIL_CONFIRMATION = 'email_confirmation'
    PASSWORD_RESET = 'password_reset'


class AuthTokenType(StrEnum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class Language(StrEnum):
    RU = 'ru'
    EN = 'en'


class Theme(StrEnum):
    WHITE = 'white'
    BLACK = 'black'
    SYSTEM = 'system'
