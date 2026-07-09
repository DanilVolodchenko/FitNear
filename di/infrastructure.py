from collections.abc import AsyncIterable

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.interfaces.localization import ITranslator
from application.interfaces.security import IHasher, IJWTToken, IPwdHasher, ITokenGenerator
from application.interfaces.token import (
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
    IRegistrationTokenUpdater,
)
from application.interfaces.transaction import TransactionManager
from application.interfaces.user import IUserReader, IUserSaver
from core.config import Config
from infrastructure.localization import Translator
from infrastructure.repositories.token import RegistrationTokenRepository
from infrastructure.repositories.user import UserRepository
from infrastructure.resources.database import new_session_maker
from infrastructure.security import Argon2PwdHasher, JWTToken, RandomTokenGenerator, SHA256Hasher


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, TransactionManager]]:
        async with session_maker() as session:
            try:
                yield session
            except Exception:  # noqa: BLE001
                await session.rollback()

    user_repository = provide(
        UserRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[IUserReader, IUserSaver],
    )

    registration_token_repository = provide(
        RegistrationTokenRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[IRegistrationTokenReader, IRegistrationTokenSaver, IRegistrationTokenUpdater],
    )

    jwt_token = provide(JWTToken, scope=Scope.APP, provides=IJWTToken)

    pwd_hasher = provide(Argon2PwdHasher, scope=Scope.APP, provides=IPwdHasher)

    sha256_hasher = provide(
        SHA256Hasher,
        scope=Scope.APP,
        provides=IHasher,
    )

    translator = provide(Translator, scope=Scope.APP, provides=ITranslator)
    random_token_generator = provide(RandomTokenGenerator, scope=Scope.APP, provides=ITokenGenerator)
