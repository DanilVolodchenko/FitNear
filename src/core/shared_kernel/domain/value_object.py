from enum import StrEnum


class UserRole(StrEnum):
    CLIENT = 'client'
    STUFF = 'stuff'
    ADMIN = 'admin'


class AuthTokenType(StrEnum):
    ACCESS = 'access'
    REFRESH = 'refresh'
