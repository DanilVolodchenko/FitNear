from dishka import Provider, Scope, provide

from application.interfaces.generator import IStringGenerator
from application.interfaces.localization import ITranslator
from application.interfaces.repositories import (
    IRegistrationTokenSaver,
    IUserReader,
    IUserRemover,
    IUserSaver,
)
from application.interfaces.security import IHasher, IPwdHasher
from application.interfaces.transaction import ITransactionManager
from application.services.auth import RegisterUserService
from core.config import Config


class ApplicationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_register_user_service(
        self,
        config: Config,
        tranlator: ITranslator,
        user_reader: IUserReader,
        user_saver: IUserSaver,
        user_remover: IUserRemover,
        reg_token_saver: IRegistrationTokenSaver,
        pwd_hasher: IPwdHasher,
        string_generator: IStringGenerator,
        hasher: IHasher,
        trx_manager: ITransactionManager,
    ) -> RegisterUserService:
        return RegisterUserService(
            config=config,
            translator=tranlator,
            user_reader=user_reader,
            user_saver=user_saver,
            user_remover=user_remover,
            reg_token_saver=reg_token_saver,
            pwd_hasher=pwd_hasher,
            string_generator=string_generator,
            hasher=hasher,
            trx_manager=trx_manager,
        )

    register_user_service = provide(RegisterUserService, scope=Scope.REQUEST)
