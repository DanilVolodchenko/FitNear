import dataclasses
from datetime import datetime
from uuid import UUID

from src.core.shared_kernel.domain.value_object import AuthTokenType


@dataclasses.dataclass(frozen=True, slots=True)
class AuthTokenDM:
    id: int
    type: AuthTokenType
    jti: UUID
    token_hash: str
    user_agent: str | None
    ip_address: str | None
    is_active: bool
    family_id: UUID | None
    expires_at: datetime
    revoked_at: datetime | None
    last_used_at: datetime | None
    created_at: datetime

    user_id: int
