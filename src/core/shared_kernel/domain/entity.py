import dataclasses
from datetime import datetime

from src.core.shared_kernel.domain.value_object import AuthTokenType


@dataclasses.dataclass(frozen=True, slots=True)
class AuthTokenDM:
    user_id: int
    type: AuthTokenType
    token_hash: str
    user_agent: str | None
    ip_address: str | None
    is_active: bool
    expires_at: datetime
    revoked_at: datetime | None
    created_at: datetime
