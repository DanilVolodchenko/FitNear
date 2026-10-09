from dataclasses import asdict
from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import insert, select, update

from src.core.components.user.application.interface import (
    IConfirmationCodeEditor,
    IConfirmationCodeReader,
    IConfirmationCodeSaver,
)
from src.core.components.user.domain.entity import ConfirmationCodeDM
from src.infrastructure.models.token import ConfirmationCode


class ConfirmationCodeRepository(IConfirmationCodeSaver, IConfirmationCodeReader, IConfirmationCodeEditor):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, confirmation_code_dm: ConfirmationCodeDM) -> None:
        stmt = insert(ConfirmationCode).values(**asdict(confirmation_code_dm))

        await self._session.execute(stmt)

    async def get_by_token_hash(self, token_hash: str) -> ConfirmationCodeDM | None:
        stmt = select(ConfirmationCode).where(ConfirmationCode.token_hash == token_hash)

        result = await self._session.execute(stmt)
        registration_token = result.scalar_one_or_none()

        if not registration_token:
            return None

        return self._to_dm(registration_token)

    async def get_by_id(self, ident: UUID) -> ConfirmationCodeDM | None:
        stmt = select(ConfirmationCode).where(ConfirmationCode.id == ident)

        result = await self._session.execute(stmt)
        registration_token = result.scalar_one_or_none()

        if not registration_token:
            return None

        return self._to_dm(registration_token)

    async def deactivate(self, ident: UUID) -> None:
        stmt = update(ConfirmationCode).where(ConfirmationCode.id == ident).values(is_active=False)

        await self._session.execute(stmt)

    def _to_dm(self, registration_token: ConfirmationCode) -> ConfirmationCodeDM:
        return ConfirmationCodeDM(
            id=registration_token.id,
            user_id=registration_token.user_id,
            code_hash=registration_token.code_hash,
            type=registration_token.type,
            is_active=registration_token.is_active,
            expires_at=registration_token.expires_at,
            created_at=registration_token.created_at,
        )
