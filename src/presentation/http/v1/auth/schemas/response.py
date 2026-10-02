from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RegisteredUserResponse(BaseModel):
    registration_id: UUID
    expires_at: datetime


class LoginUserResponse(BaseModel):
    access: str
    type: str = 'bearer'
