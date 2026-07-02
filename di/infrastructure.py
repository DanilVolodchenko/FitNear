from collections.abc import AsyncIterable

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.interfaces.localization import ITranslator
from application.interfaces.security import IHasher, IJWTToken, IPwdHasher
from application.interfaces.transaction import TransactionManager
from application.interfaces.user import IUserReader, IUserSaver
from core.config import Config
from infrastructure.localization import Translator
from infrastructure.repositories.user import UserRepository
from infrastructure.resources.database import new_session_maker
from infrastructure.security import Argon2PwdHasher, JWTToken, SHA256Hasher


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
            except Exception:
                await session.rollback()

    user_repository = provide(
        UserRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[IUserReader, IUserSaver],
    )

    jwt_token = provide(JWTToken, scope=Scope.APP, provides=IJWTToken)

    pwd_hasher = provide(Argon2PwdHasher, scope=Scope.APP, provides=IPwdHasher)

    sha256_hasher = provide(
        SHA256Hasher,
        scope=Scope.APP,
        provides=IHasher,
    )

    translator = provide(Translator, scope=Scope.APP, provides=ITranslator)
