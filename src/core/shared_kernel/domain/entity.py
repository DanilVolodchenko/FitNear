import dataclasses
from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from src.core.shared_kernel.domain.value_object import AuthTokenType


@dataclasses.dataclass(frozen=True, slots=True)
class AuthTokenDM:
    id: UUID
    type: AuthTokenType
    token_hash: str
    user_agent: str | None
    ip_address: str | None
    is_active: bool
    family_id: UUID | None
    expires_at: datetime
    revoked_at: datetime | None
    last_used_at: datetime | None
    created_at: datetime

    user_id: UUID

    @classmethod
    def create(
        cls,
        ident: UUID,
        token_type: AuthTokenType,
        token_hash: str,
        user_agent: str | None,
        ip_address: str | None,
        family_id: UUID | None,
        expires_at: datetime,
        user_id: UUID,
    ) -> Self:
        return cls(
            id=ident,
            type=token_type,
            token_hash=token_hash,
            user_agent=user_agent,
            ip_address=ip_address,
            is_active=True,
            family_id=family_id,
            expires_at=expires_at,
            revoked_at=None,
            last_used_at=None,
            created_at=datetime.now(tz=UTC),
            user_id=user_id,
        )
