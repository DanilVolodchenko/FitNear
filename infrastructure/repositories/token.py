from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text

from application.domain.entities.token import RegistrationTokenDM
from application.dto.token import CreateRegisterTokenDTO
from application.interfaces.repositories import (
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
)


class RegistrationTokenRepository(IRegistrationTokenReader, IRegistrationTokenSaver):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_token_hash(self, token_hash: str) -> RegistrationTokenDM | None:
        stmt = text('SELECT * FROM registration_token WHERE token_hash = :token_hash')

        result = await self._session.execute(statement=stmt, params={'token_hash': token_hash})

        entity = result.mappings().one_or_none()

        if not entity:
            return None

        return RegistrationTokenDM(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            type=entity.type,
            active=entity.active,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )

    async def create(self, token_dto: CreateRegisterTokenDTO) -> RegistrationTokenDM:
        stmt = text(
            """
            INSERT INTO registration_tokens (user_id, token_hash, type, active, expires_at)
            VALUES (:user_id, :token_hash, :type, :active, :expires_at)
            RETURNING *
            """  # ruff: ignore[missing-trailing-comma]
        )

        result = await self._session.execute(
            statement=stmt,
            params={
                'user_id': token_dto.user_id,
                'token_hash': token_dto.token_hash,
                'type': token_dto.type,
                'active': token_dto.active,
                'expires_at': token_dto.expires_at,
            },
        )

        entity = result.mappings().one()

        return RegistrationTokenDM(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            type=entity.type,
            active=entity.active,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )
