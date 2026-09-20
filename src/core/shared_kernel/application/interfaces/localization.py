from abc import ABC, abstractmethod
from pathlib import Path

from fastapi import Request


class ITranslator(ABC):
    @abstractmethod
    def translate(self, text: str, lang_code: str) -> str:
        """
        Localize to certain language.
        :param text: Text to translate;
        :param lang_code: Language code like: ru_RU/en_GB;
        :returns: Translation string.
        """

    @abstractmethod
    def get_lang_code(self, request: Request) -> str:
        """
        Return lang_code from request obj.
        :param request: request from client.
        :returns: Language code.
        """

    @abstractmethod
    def compile(self, i18n_path: Path) -> None:
        """
        Compile localization files.
        :param i18n_path: Path to i18n dir.
        :returns: None
        """

    @abstractmethod
    def init_new_language(self, lang_code: str) -> None:
        """
        Init new language translation.
        params lang_code: Language code.
        returns: None.
        """
