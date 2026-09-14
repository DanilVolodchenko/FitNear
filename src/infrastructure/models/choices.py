from enum import StrEnum


class RegistrationTokenType(StrEnum):
    EMAIL_CONFIRMATION = 'EMAIL_CONFIRMATION'
    PASSWORD_RESET = 'PASSWORD_RESET'  # noqa: S105


class AuthTokenType(StrEnum):
    REFRESH = 'REFRESH'


class LanguageType(StrEnum):
    RU = 'RU'
    EN = 'EN'


class ThemeType(StrEnum):
    WHITE = 'WHITE'
    BLACK = 'BLACK'
