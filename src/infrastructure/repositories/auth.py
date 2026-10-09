from dataclasses import asdict
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.core.shared_kernel.application.interfaces.token import (
    IRefreshTokenEditor,
    IRefreshTokenReader,
    IRefreshTokenSaver,
)
from src.core.shared_kernel.domain.entity import RefreshTokenDM
from src.infrastructure.models.token import RefreshToken


class RefreshTokenRepository(IRefreshTokenSaver, IRefreshTokenReader, IRefreshTokenEditor):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, refresh_token_dm: RefreshTokenDM) -> None:
        stmt = insert(RefreshToken).values(**asdict(refresh_token_dm))

        await self._session.execute(stmt)

    async def get_by_id(self, ident: UUID) -> RefreshTokenDM | None:
        stmt = select(RefreshToken).where(RefreshToken.id == ident)

        result = await self._session.execute(stmt)
        auth_token = result.scalar_one_or_none()

        if not auth_token:
            return None

        return self._to_dm(auth_token)

    async def deactivate_by_id(self, ident: UUID) -> None:
        stmt = update(RefreshToken).where(RefreshToken.id == ident).values(is_active=False)

        await self._session.execute(stmt)

    def _to_dm(self, refresh_token: RefreshToken) -> RefreshTokenDM:
        return RefreshTokenDM(
            id=refresh_token.id,
            token_hash=refresh_token.token_hash,
            user_agent=refresh_token.user_agent,
            ip_address=refresh_token.ip_address,
            is_active=refresh_token.is_active,
            family_id=refresh_token.family_id,
            expires_at=refresh_token.expires_at,
            revoked_at=refresh_token.revoked_at,
            last_used_at=refresh_token.last_used_at,
            created_at=refresh_token.created_at,
            user_id=refresh_token.user_id,
        )
