from collections.abc import AsyncIterable
from dishka import Provider, Scope, AnyOf, provide
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from core.config import Config
from infrastructure.resources.database import new_session_maker
from infrastructure.repositories.user import UserRepository
from infrastructure.security import JWTToken, Argon2PwdHasher, SHA256Hasher
from application.interfaces.user import IUserReader, IUserSaver
from application.interfaces.security import IJWTToken, IPwdHasher, IHasher
from application.interfaces.transaction import TransactionManager


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

    jwt_token = provide(
        JWTToken,
        scope=Scope.APP,
        provides=IJWTToken
    )

    pwd_hasher = provide(
        Argon2PwdHasher,
        scope=Scope.APP,
        provides=IPwdHasher
    )

    sha256_hasher = provide(
        SHA256Hasher,
        scope=Scope.APP,
        provides=IHasher,
    )
