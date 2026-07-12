from collections.abc import AsyncIterable

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.interfaces.generator import IStringGenerator
from application.interfaces.localization import ITranslator
from application.interfaces.repositories import (
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
    IRegistrationTokenUpdater,
    IUserReader,
    IUserRemover,
    IUserSaver,
)
from application.interfaces.security import IHasher, IJWTToken, IPwdHasher
from application.interfaces.template import IHTMLTemplate
from application.interfaces.transaction import ITransactionManager
from core.config import Config
from infrastructure.generator import RandomStringGenerator
from infrastructure.localization import Translator
from infrastructure.repositories.token import RegistrationTokenRepository
from infrastructure.repositories.user import UserRepository
from infrastructure.resources.database import new_session_maker
from infrastructure.security import Argon2PwdHasher, JWTToken, SHA256Hasher
from infrastructure.template import HTMLTemplate


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

    user_repository = provide(
        UserRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[IUserReader, IUserSaver, IUserRemover],
    )

    registration_token_repository = provide(
        RegistrationTokenRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[IRegistrationTokenReader, IRegistrationTokenSaver, IRegistrationTokenUpdater],
    )

    jwt_token = provide(JWTToken, scope=Scope.APP, provides=IJWTToken)

    pwd_hasher = provide(Argon2PwdHasher, scope=Scope.APP, provides=IPwdHasher)

    sha256_hasher = provide(SHA256Hasher, scope=Scope.APP, provides=IHasher)

    translator = provide(Translator, scope=Scope.APP, provides=ITranslator)

    random_string_generator = provide(RandomStringGenerator, scope=Scope.APP, provides=IStringGenerator)

    html_template = provide(HTMLTemplate, scope=Scope.APP, provides=IHTMLTemplate)
