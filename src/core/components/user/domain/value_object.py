from enum import StrEnum


class ConfirmationCodeType(StrEnum):
    EMAIL = 'email'


class Language(StrEnum):
    RU = 'ru'
    EN = 'en'


class Theme(StrEnum):
    WHITE = 'white'
    BLACK = 'black'
