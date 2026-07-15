import gettext
from pathlib import Path

from babel.messages.frontend import CommandLineInterface
from starlette.requests import Request

from config.config_path import I18N_PATH
from src.core.interfaces.localization import ITranslator


class Translator(ITranslator):
    def __init__(self) -> None:
        self._command_line = CommandLineInterface()

    def translate(self, text: str, lang_code: str) -> str:
        translation = gettext.translation('messages', I18N_PATH, languages=[lang_code], fallback=True)

        return translation.gettext(text)

    def get_lang_code(self, request: Request) -> str:
        accept_language = request.headers.get('accept-language', 'ru_RU')
        lang_code = accept_language.split(',')[0]

        return lang_code.replace('-', '_')

    def compile(self, i18n_path: Path) -> None:
        command = ['pybabel', 'compile', '-d', i18n_path]

        self._command_line.run(command)

    def init_new_language(self, lang_code: str) -> None:
        command = ['pybabel', 'init', '-l', lang_code, '-i', 'i18n/messages.pot', '-d', 'i18n']

        self._command_line.run(command)
