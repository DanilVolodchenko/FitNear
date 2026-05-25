from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio.session import AsyncSession

from application.interfaces.user import IUserReader, IUserSaver
from domain.entities.user import UserDM
from application.dto.user import CreateUserDTO


class UserRepository(IUserReader, IUserSaver):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_username(self, username: str) -> UserDM | None:
        stmt = text('SELECT * FROM users WHERE username = :username')

        result = await self._session.execute(
            statement=stmt,
            params={'username': username},
        )
        row = result.fetchone()
        if not row:
            return None

        return UserDM(
            id=row.id,
            username=row.username,
            name=row.name,
            password=row.password,
        )

    async def create(self, user: CreateUserDTO) -> UserDM:
        stmt = text(
            """
            INSERT INTO users (username, name, password)
            VALUES (:username, :name, :password)
            RETURNING id;
            """
        )

        result = await self._session.execute(
            statement=stmt,
            params={
                'username': user.username,
                'name': user.name,
                'password': user.password,
            }
        )

        user_id = result.scalar_one()

        return UserDM(
            id=user_id,
            username=user.username,
            name=user.name,
            password=user.password,
        )
