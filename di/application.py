from dishka import Provider, Scope, provide

from config import Config
from src.core.interfaces.generator import IStringGenerator
from src.core.interfaces.repositories import (
    IRegistrationTokenEditor,
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
    IUserEditor,
    IUserReader,
    IUserRemover,
    IUserSaver,
)
from src.core.interfaces.security import IHasher, IPwdHasher
from src.core.interfaces.transaction import ITransactionManager
from src.core.services.user import ConfirmUserService, RegisterUserService


class ApplicationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_register_user_service(
        self,
        config: Config,
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
            user_reader=user_reader,
            user_saver=user_saver,
            user_remover=user_remover,
            reg_token_saver=reg_token_saver,
            pwd_hasher=pwd_hasher,
            string_generator=string_generator,
            hasher=hasher,
            trx_manager=trx_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def get_confirm_user_service(
        self,
        config: Config,
        user_reader: IUserReader,
        user_editor: IUserEditor,
        user_remover: IUserRemover,
        reg_token_reader: IRegistrationTokenReader,
        reg_token_editor: IRegistrationTokenEditor,
        pwd_hasher: IPwdHasher,
        string_generator: IStringGenerator,
        hasher: IHasher,
        trx_manager: ITransactionManager,
    ) -> ConfirmUserService:
        return ConfirmUserService(
            config=config,
            user_reader=user_reader,
            user_editor=user_editor,
            reg_token_reader=reg_token_reader,
            reg_token_editor=reg_token_editor,
            hasher=hasher,
            trx_manager=trx_manager,
        )

    register_user_service = provide(RegisterUserService, scope=Scope.REQUEST)
