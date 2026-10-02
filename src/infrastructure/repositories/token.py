from dataclasses import asdict
from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import insert, select, update

from src.core.components.user.application.interface import (
    IRegistrationTokenEditor,
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
)
from src.core.components.user.domain.entity import RegistrationTokenDM
from src.infrastructure.models.token import RegistrationToken


class RegistrationTokenRepository(IRegistrationTokenSaver, IRegistrationTokenReader, IRegistrationTokenEditor):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, token_dm: RegistrationTokenDM) -> None:
        stmt = insert(RegistrationToken).values(**asdict(token_dm))

        await self._session.execute(stmt)

    async def get_by_token_hash(self, token_hash: str) -> RegistrationTokenDM | None:
        stmt = select(RegistrationToken).where(RegistrationToken.token_hash == token_hash)

        result = await self._session.execute(stmt)
        registration_token = result.scalar_one_or_none()

        if not registration_token:
            return None

        return self._to_dm(registration_token)

    async def get_by_id(self, ident: UUID) -> RegistrationTokenDM | None:
        stmt = select(RegistrationToken).where(RegistrationToken.id == ident)

        result = await self._session.execute(stmt)
        registration_token = result.scalar_one_or_none()

        if not registration_token:
            return None

        return self._to_dm(registration_token)

    async def deactivate(self, ident: UUID) -> None:
        stmt = update(RegistrationToken).where(RegistrationToken.id == ident).values(is_active=False)

        await self._session.execute(stmt)

    def _to_dm(self, registration_token: RegistrationToken) -> RegistrationTokenDM:
        return RegistrationTokenDM(
            id=registration_token.id,
            user_id=registration_token.user_id,
            token_hash=registration_token.token_hash,
            type=registration_token.type,
            is_active=registration_token.is_active,
            expires_at=registration_token.expires_at,
            created_at=registration_token.created_at,
        )
