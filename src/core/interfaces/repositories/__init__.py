__all__ = [
    'IRegistrationTokenEditor',
    'IRegistrationTokenReader',
    'IRegistrationTokenSaver',
    'IUserEditor',
    'IUserReader',
    'IUserRemover',
    'IUserSaver',
]

from src.core.interfaces.repositories.token import (
    IRegistrationTokenEditor,
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
)
from src.core.interfaces.repositories.user import IUserEditor, IUserReader, IUserRemover, IUserSaver
