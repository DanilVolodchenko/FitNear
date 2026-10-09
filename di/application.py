from dishka import Provider, Scope, provide

from config import Config
from src.core.components.user.application.interface import (
    IConfirmationCodeEditor,
    IConfirmationCodeReader,
    IConfirmationCodeSaver,
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
from src.core.shared_kernel.application.interfaces.token import (
    IRefreshTokenEditor,
    IRefreshTokenReader,
    IRefreshTokenSaver,
)
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
        confirmation_code_saver: IConfirmationCodeSaver,
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
            confirmation_code_saver=confirmation_code_saver,
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
        confirmation_code_reader: IConfirmationCodeReader,
        confirmation_code_editor: IConfirmationCodeEditor,
        hasher: IHasher,
        trx_manager: ITransactionManager,
    ) -> ConfirmUserService:
        return ConfirmUserService(
            config=config,
            user_editor=user_editor,
            confirmation_code_reader=confirmation_code_reader,
            confirmation_code_editor=confirmation_code_editor,
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
        refresh_token_saver: IRefreshTokenSaver,
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
            refresh_token_saver=refresh_token_saver,
            trx_manager=trx_manager,
        )

    @provide(scope=Scope.REQUEST)
    async def get_logout_user_service(
        self,
        config: Config,
        refresh_token_reader: IRefreshTokenReader,
        refresh_token_editor: IRefreshTokenEditor,
        jwt_token: IJWTToken,
        trx_manager: ITransactionManager,
    ) -> LogoutUserService:
        return LogoutUserService(
            security_config=config.security,
            refresh_token_reader=refresh_token_reader,
            refresh_token_editor=refresh_token_editor,
            jwt_token=jwt_token,
            trx_manager=trx_manager,
        )
