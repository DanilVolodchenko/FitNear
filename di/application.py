from dishka import Provider, Scope, provide

from config import Config
from src.core.components.user.application.interface import (
    IRegistrationTokenEditor,
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
    ISettingsSaver,
    IUserEditor,
    IUserReader,
    IUserRemover,
    IUserSaver,
)
from src.core.components.user.application.service import (
    ConfirmUserService,
    LoginUserService,
    LogoutUserService,
    RegisterUserService,
)
from src.core.shared_kernel.application.interfaces.security import IHasher, IJWTToken
from src.core.shared_kernel.application.interfaces.token import IAuthTokenSaver, IAuthTokenEditor, IAuthTokenReader
from src.core.shared_kernel.application.interfaces.transaction import ITransactionManager
from src.infrastructure.event_bus.taskiq import TaskiqEventBus
from src.infrastructure.generator import StringDigitCodeGenerator, UUID4Generator, UUID7Generator
from src.infrastructure.security import Argon2PwdHasher, SHA256Hasher


class ApplicationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_register_user_service(
        self,
        config: Config,
        user_reader: IUserReader,
        user_saver: IUserSaver,
        user_remover: IUserRemover,
        settings_saver: ISettingsSaver,
        reg_token_saver: IRegistrationTokenSaver,
        pwd_hasher: Argon2PwdHasher,
        uuid_generator: UUID7Generator,
        string_generator: StringDigitCodeGenerator,
        hasher: SHA256Hasher,
        trx_manager: ITransactionManager,
        event_bus: TaskiqEventBus,
    ) -> RegisterUserService:
        return RegisterUserService(
            security_config=config.security,
            server_config=config.server,
            user_reader=user_reader,
            user_saver=user_saver,
            user_remover=user_remover,
            settings_saver=settings_saver,
            reg_token_saver=reg_token_saver,
            pwd_hasher=pwd_hasher,
            uuid_generator=uuid_generator,
            string_generator=string_generator,
            hasher=hasher,
            trx_manager=trx_manager,
            event_bus=event_bus,
        )

    @provide(scope=Scope.REQUEST)
    async def get_confirm_user_service(
        self,
        config: Config,
        user_editor: IUserEditor,
        reg_token_reader: IRegistrationTokenReader,
        reg_token_editor: IRegistrationTokenEditor,
        hasher: IHasher,
        trx_manager: ITransactionManager,
    ) -> ConfirmUserService:
        return ConfirmUserService(
            config=config,
            user_editor=user_editor,
            reg_token_reader=reg_token_reader,
            reg_token_editor=reg_token_editor,
            hasher=hasher,
            trx_manager=trx_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def get_login_user_service(
        self,
        config: Config,
        user_reader: IUserReader,
        pwd_hasher: Argon2PwdHasher,
        uuid4_generator: UUID4Generator,
        uuid7_generator: UUID7Generator,
        jwt_token: IJWTToken,
        hasher: IHasher,
        auth_token_saver: IAuthTokenSaver,
        trx_manager: ITransactionManager,
    ) -> LoginUserService:
        return LoginUserService(
            security_config=config.security,
            user_reader=user_reader,
            pwd_hasher=pwd_hasher,
            uuid4_generator=uuid4_generator,
            uuid7_generator=uuid7_generator,
            jwt_token=jwt_token,
            hasher=hasher,
            auth_token_saver=auth_token_saver,
            trx_manager=trx_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def get_logout_user_service(
        self,
        config: Config,
        auth_token_reader: IAuthTokenReader,
        auth_token_editor: IAuthTokenEditor,
        jwt_token: IJWTToken,
        trx_manager: ITransactionManager,
    ) -> LogoutUserService:
        return LogoutUserService(
            security_config=config.security,
            auth_token_reader=auth_token_reader,
            auth_token_editor=auth_token_editor,
            jwt_token=jwt_token,
            trx_manager=trx_manager,
        )
