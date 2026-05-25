import abc


class ITokenReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_(self):
        ...


class ITokenSaver(abc.ABC):
    @abc.abstractmethod
    async def create(self) -> None:
        """"""
