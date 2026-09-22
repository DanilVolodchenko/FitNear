from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.core.shared_kernel.application.dto.token import CreateAuthTokenDTO
from src.core.shared_kernel.application.interfaces.auth import IAuthTokenEditor, IAuthTokenReader, IAuthTokenSaver
from src.core.shared_kernel.domain.entity import AuthTokenDM
from src.infrastructure.models.token import AuthToken


class AuthTokenRepository(IAuthTokenSaver, IAuthTokenReader, IAuthTokenEditor):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, create_token_dto: CreateAuthTokenDTO) -> AuthTokenDM:
        stmt = (
            insert(AuthToken)
            .values(
                type=create_token_dto.type,
                jti=create_token_dto.jti,
                token_hash=create_token_dto.token_hash,
                user_agent=create_token_dto.user_agent,
                ip_address=create_token_dto.ip_address,
                family_id=create_token_dto.family_id,
                expires_at=create_token_dto.expires_at,
                user_id=create_token_dto.user_id,
            )
            .returning(AuthToken)
        )

        result = await self._session.execute(stmt)
        auth_token = result.scalar_one()

        return self._to_dm(auth_token)

    async def get_by_id(self, ident: int) -> AuthTokenDM | None:
        stmt = select(AuthToken).where(AuthToken.id == ident)

        result = await self._session.execute(stmt)
        auth_token = result.scalar_one_or_none()

        if not auth_token:
            return None

        return self._to_dm(auth_token)

    async def deactivate_by_id(self, ident: int) -> None:
        stmt = update(AuthToken).where(AuthToken.id == ident).values(is_active=False)

        await self._session.execute(stmt)

    def _to_dm(self, auth_token: AuthToken) -> AuthTokenDM:
        return AuthTokenDM(
            id=auth_token.id,
            type=auth_token.type,
            jti=auth_token.jti,
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
