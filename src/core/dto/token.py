from dataclasses import dataclass
from datetime import datetime

from src.core.domain.entities.token import RegistrationTokenType


@dataclass(frozen=True, slots=True)
class CreateRegisterTokenDTO:
    user_id: int
    token_hash: str
    type: RegistrationTokenType
    expires_at: datetime
    active: bool = True
