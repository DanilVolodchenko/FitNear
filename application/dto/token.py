from dataclasses import dataclass
from datetime import datetime

from application.domain.entities.token import RegistrationTokenType


@dataclass(slots=True)
class CreateRegisterTokenDTO:
    user_id: int
    token_hash: str
    type: RegistrationTokenType
    expires_at: datetime
    active: bool = True
