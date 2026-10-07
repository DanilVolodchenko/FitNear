from dataclasses import asdict
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.core.shared_kernel.application.interfaces.token import IAuthTokenEditor, IAuthTokenReader, IAuthTokenSaver
from src.core.shared_kernel.domain.entity import AuthTokenDM
from src.infrastructure.models.token import AuthToken


class AuthTokenRepository(IAuthTokenSaver, IAuthTokenReader, IAuthTokenEditor):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, auth_token_dm: AuthTokenDM) -> None:
        stmt = insert(AuthToken).values(**asdict(auth_token_dm))

        await self._session.execute(stmt)

    async def get_by_id(self, ident: UUID) -> AuthTokenDM | None:
        stmt = select(AuthToken).where(AuthToken.id == ident)

        result = await self._session.execute(stmt)
        auth_token = result.scalar_one_or_none()

        if not auth_token:
            return None

        return self._to_dm(auth_token)

    async def deactivate_by_id(self, ident: UUID) -> None:
        stmt = update(AuthToken).where(AuthToken.id == ident).values(is_active=False)

        await self._session.execute(stmt)

    def _to_dm(self, auth_token: AuthToken) -> AuthTokenDM:
        return AuthTokenDM(
            id=auth_token.id,
            type=auth_token.type,
            token_hash=auth_token.token_hash,
            user_agent=auth_token.user_agent,
            ip_address=auth_token.ip_address,
            is_active=auth_token.is_active,
            family_id=auth_token.family_id,
            expires_at=auth_token.expires_at,
            revoked_at=auth_token.revoked_at,
            last_used_at=auth_token.last_used_at,
            created_at=auth_token.created_at,
            user_id=auth_token.user_id,
        )
