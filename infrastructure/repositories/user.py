from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text

from application.dto.user import CreateUserDTO
from application.interfaces.user import IUserReader, IUserSaver
from domain.entities.user import UserDM


class UserRepository(IUserReader, IUserSaver):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> UserDM | None:
        stmt = text('SELECT * FROM users WHERE email = :email')

        result = await self._session.execute(
            statement=stmt,
            params={'email': email},
        )
        row = result.fetchone()

        if not row:
            return None

        return UserDM(
            id=row.id,
            email=row.email,
            name=row.name,
            password=row.password,
            is_comfirmed=row.is_confirmed,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def create(self, user: CreateUserDTO) -> int:
        stmt = text(
            """
            INSERT INTO users (email, name, password, is_confirmed)
            VALUES (:email, :name, :password, :is_confirmed)
            RETURNING id;
            """
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

        user_id: int = result.scalar_one()

        return user_id
