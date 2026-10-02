import dataclasses
from datetime import datetime
from uuid import UUID

from src.core.shared_kernel.domain.value_object import AuthTokenType


@dataclasses.dataclass(frozen=True, slots=True)
class CreateAuthTokenDTO:
    type: AuthTokenType
    jti: UUID
    token_hash: str
    user_agent: str | None
    ip_address: str | None
    family_id: UUID | None
    expires_at: datetime

    user_id: UUID
