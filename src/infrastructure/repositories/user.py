from dataclasses import asdict

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import delete, insert, select, update

from src.core.components.user.application.interface import (
    ISettingsSaver,
    IUserEditor,
    IUserReader,
    IUserRemover,
    IUserSaver,
)
from src.core.components.user.domain.entity import SettingsDM, UserDM
from src.infrastructure.models.user import Settings, User


class UserRepository(IUserSaver, IUserReader, IUserEditor, IUserRemover):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user_dm: UserDM) -> None:
        stmt = insert(User).values(**asdict(user_dm))

        await self._session.execute(statement=stmt)

    async def get_by_id(self, ident: int) -> UserDM | None:
        stmt = select(User).where(User.id == ident)

        result = await self._session.execute(statement=stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        return self._to_dm(user)

    async def get_by_email(self, email: str) -> UserDM | None:
        stmt = select(User).where(User.email == email)

        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        return self._to_dm(user)

    async def confirm_user_email(self, user_id: int) -> None:
        stmt = update(User).where(User.id == user_id).values(is_confirmed=True)

        await self._session.execute(statement=stmt)

    async def remove_by_email(self, email: str) -> None:
        stmt = delete(User).where(User.email == email)

        await self._session.execute(stmt)

    def _to_dm(self, user: User) -> UserDM:
        return UserDM(
            id=user.id,
            email=user.email,
            role=user.role,
            name=user.name,
            hashed_password=user.hashed_password,
            is_confirmed=user.is_confirmed,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class SettingsRepository(ISettingsSaver):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, settings_dm: SettingsDM) -> None:
        stmt = insert(Settings).values(**asdict(settings_dm))

        await self._session.execute(stmt)
