import dataclasses
from datetime import datetime

from core.shared_kernel.domain.value_object import AuthTokenType


@dataclasses.dataclass(frozen=True, slots=True)
class CreateAuthTokenDTO:
    user_id: int
    type: AuthTokenType
    token_hash: str
    user_agent: str | None
    ip_address: str | None
    expires_at: datetime
