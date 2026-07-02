import abc


class ITranslator(abc.ABC):
    @abc.abstractmethod
    def translate(self, text: str, *, lang: str) -> str:
        """
        Localize to certain language.
        :param text: Text to translate;
        :param lang: Language;
        :return Translation.
        """
