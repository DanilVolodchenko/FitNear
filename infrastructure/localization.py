import gettext

from babel.messages.frontend import CommandLineInterface

from application.interfaces.localization import ITranslator
from core.config_path import I18N_PATH


class Translator(ITranslator):
    def translate(self, text: str, lang: str) -> str:
        translation = gettext.translation('messages', I18N_PATH, languages=[lang], fallback=True)

        return translation.gettext(text)


def compile_translations() -> None:
    """Compile translations."""

    args = ['pybabel', 'compile', '-d', I18N_PATH]

    CommandLineInterface().run(args)


def init_new_translation(lang: str) -> None:
    """Create new translation."""

    args = ['pybabel', 'init', '-l', lang, '-i', 'i18n/messages.pot', '-d', 'i18n']

    CommandLineInterface().run(args)
