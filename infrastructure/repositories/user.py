from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text

from application.domain.entities.user import UserDM
from application.dto.user import CreateUserDTO
from application.interfaces.user import IUserReader, IUserSaver


class UserRepository(IUserReader, IUserSaver):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

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
