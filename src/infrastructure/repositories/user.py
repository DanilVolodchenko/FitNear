from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text

from src.core.domain.entities.user import UserDM
from src.core.dto.user import CreateUserDTO
from src.core.interfaces.repositories import IUserEditor, IUserReader, IUserRemover, IUserSaver


class UserRepository(IUserReader, IUserSaver, IUserEditor, IUserRemover):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, ident: int) -> UserDM | None:
        stmt = text('SELECT * FROM users WHERE id = :id')

        result = await self._session.execute(
            statement=stmt,
            params={'id': ident},
        )
        entity = result.mappings().one_or_none()

        if not entity:
            return None

        return UserDM(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            password=entity.password,
            is_confirmed=entity.is_confirmed,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def get_by_email(self, email: str) -> UserDM | None:
        stmt = text('SELECT * FROM users WHERE email = :email')

        result = await self._session.execute(
            statement=stmt,
            params={'email': email},
        )
        entity = result.mappings().one_or_none()

        if not entity:
            return None

        return UserDM(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            password=entity.password,
            is_confirmed=entity.is_confirmed,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, user: CreateUserDTO) -> UserDM:
        stmt = text(
            """
            INSERT INTO users (email, name, password, is_confirmed)
            VALUES (:email, :name, :password, :is_confirmed)
            RETURNING *;
            """  # ruff: ignore[missing-trailing-comma]
        )

        result = await self._session.execute(
            statement=stmt,
            params={
                'email': user.email,
                'name': user.name,
                'password': user.password,
                'is_confirmed': user.is_confirmed,
            },
        )

        entity = result.mappings().one()

        return UserDM(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            password=entity.password,
            is_confirmed=entity.is_confirmed,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def confirm_user_email(self, user_id: int) -> None:
        stmt = text('UPDATE users SET is_confirmed = true WHERE id = :id')

        await self._session.execute(
            statement=stmt,
            params={'id': user_id},
        )

    async def remove_by_email(self, email: str) -> None:
        stmt = text('DELETE FROM users WHERE email = :email')

        await self._session.execute(statement=stmt, params={'email': email})
