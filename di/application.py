from dishka import Provider, Scope, provide

from config import Config
from src.core.components.user.application.interface import (
    IRegistrationTokenEditor,
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
    IUserEditor,
    IUserReader,
    IUserRemover,
    IUserSaver,
)
from src.core.components.user.application.use_case import ConfirmUseUseCase, RegisterUserUseCase
from src.core.interfaces.generator import IStringGenerator
from src.core.interfaces.security import IHasher, IPwdHasher
from src.core.interfaces.transaction import ITransactionManager
from src.infrastructure.communication import SMTPEmailSender
from src.infrastructure.generator import StringDigitCodeGenerator
from src.infrastructure.security import Argon2PwdHasher, SHA256Hasher


class ApplicationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_register_user_use_case(
        self,
        config: Config,
        user_reader: IUserReader,
        user_saver: IUserSaver,
        user_remover: IUserRemover,
        reg_token_saver: IRegistrationTokenSaver,
        pwd_hasher: Argon2PwdHasher,
        string_generator: StringDigitCodeGenerator,
        hasher: SHA256Hasher,
        trx_manager: ITransactionManager,
        email_sender: SMTPEmailSender,
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(
            security_config=config.security,
            server_cofig=config.server,
            user_reader=user_reader,
            user_saver=user_saver,
            user_remover=user_remover,
            reg_token_saver=reg_token_saver,
            pwd_hasher=pwd_hasher,
            string_generator=string_generator,
            hasher=hasher,
            trx_manager=trx_manager,
            email_sender=email_sender,
        )

    @provide(scope=Scope.REQUEST)
    async def get_confirm_user_use_case(
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
    ) -> ConfirmUseUseCase:
        return ConfirmUseUseCase(
            config=config,
            user_reader=user_reader,
            user_editor=user_editor,
            reg_token_reader=reg_token_reader,
            reg_token_editor=reg_token_editor,
            hasher=hasher,
            trx_manager=trx_manager,
        )
