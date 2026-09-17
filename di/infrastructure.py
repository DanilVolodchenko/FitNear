from collections.abc import AsyncIterable
from typing import cast

from dishka import AnyOf, Provider, Scope, provide
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

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
from src.core.shared_kernel.application.interfaces.event_bus import IEventBus
from src.core.shared_kernel.application.interfaces.generator import IStringGenerator
from src.core.shared_kernel.application.interfaces.localization import ITranslator
from src.core.shared_kernel.application.interfaces.log import ILogger
from src.core.shared_kernel.application.interfaces.security import IHasher, IJWTToken, IPwdHasher
from src.core.shared_kernel.application.interfaces.transaction import ITransactionManager
from src.infrastructure.communication import SMTPEmailSender
from src.infrastructure.event_bus.taskiq import TaskiqEventBus
from src.infrastructure.generator import StringDigitCodeGenerator
from src.infrastructure.localization import Translator
from src.infrastructure.repositories.token import RegistrationTokenRepository
from src.infrastructure.repositories.user import SettingsRepository, UserRepository
from src.infrastructure.resources.database import new_session_maker
from src.infrastructure.security import Argon2PwdHasher, JWTToken, SHA256Hasher


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AnyOf[AsyncSession, ITransactionManager]]:
        async with session_maker() as session:
            try:
                yield session
            except Exception:  # ruff: ignore[blind-except]
                await session.rollback()

    @provide(scope=Scope.APP)
    def get_logger(self) -> ILogger:
        return cast(ILogger, logger)

    user_repository = provide(
        UserRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[UserRepository, IUserReader, IUserSaver, IUserRemover, IUserEditor],
    )

    settings_repository = provide(
        SettingsRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[SettingsRepository, ISettingsSaver],
    )

    registration_token_repository = provide(
        RegistrationTokenRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[IRegistrationTokenReader, IRegistrationTokenSaver, IRegistrationTokenEditor],
    )

    jwt_token = provide(JWTToken, scope=Scope.APP, provides=AnyOf[JWTToken, IJWTToken])

    pwd_hasher = provide(Argon2PwdHasher, scope=Scope.APP, provides=AnyOf[Argon2PwdHasher, IPwdHasher])

    sha256_hasher = provide(SHA256Hasher, scope=Scope.APP, provides=AnyOf[SHA256Hasher, IHasher])

    translator = provide(Translator, scope=Scope.APP, provides=AnyOf[Translator, ITranslator])

    @provide(scope=Scope.APP)
    async def get_smtp_email_sender(self, config: Config) -> SMTPEmailSender:
        return SMTPEmailSender(smtp_config=config.smtp)

    random_string_generator = provide(
        StringDigitCodeGenerator,
        scope=Scope.APP,
        provides=AnyOf[StringDigitCodeGenerator, IStringGenerator],
    )

    taskiq_event_bus = provide(TaskiqEventBus, scope=Scope.APP, provides=AnyOf[TaskiqEventBus, IEventBus])
