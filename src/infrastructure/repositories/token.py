from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import insert, select, update

from src.core.components.user.application.dto import CreateRegisterTokenDTO
from src.core.components.user.application.interface import (
    IRegistrationTokenEditor,
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
)
from src.core.components.user.domain.entity import RegistrationTokenDM
from src.infrastructure.models.token import RegistrationToken


class RegistrationTokenRepository(IRegistrationTokenReader, IRegistrationTokenSaver, IRegistrationTokenEditor):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_token_hash(self, token_hash: str) -> RegistrationTokenDM | None:
        stmt = select(RegistrationToken).where(RegistrationToken.token_hash == token_hash)

        result = await self._session.execute(stmt)
        registration_token = result.scalar_one_or_none()

        if not registration_token:
            return None

        return self._to_dm(registration_token)

    async def get_by_id(self, ident: int) -> RegistrationTokenDM | None:
        stmt = select(RegistrationToken).where(RegistrationToken.id == ident)

        result = await self._session.execute(stmt)
        registration_token = result.scalar_one_or_none()

        if not registration_token:
            return None

        return self._to_dm(registration_token)

    async def create(self, token_dto: CreateRegisterTokenDTO) -> RegistrationTokenDM:
        stmt = (
            insert(RegistrationToken)
            .values(
                user_id=token_dto.user_id,
                token_hash=token_dto.token_hash,
                type=token_dto.type,
                expires_at=token_dto.expires_at,
            )
            .returning(RegistrationToken)
        )

        result = await self._session.execute(stmt)
        registration_token = result.scalar_one()

        return self._to_dm(registration_token)

    async def deactivate(self, ident: int) -> None:
        stmt = update(RegistrationToken).where(RegistrationToken.id == ident).values(is_active=True)

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
