from datetime import datetime

from pydantic import BaseModel


class RegisteredUserResponse(BaseModel):
    registration_id: int
    expires_at: datetime


class LoginUserResponse(BaseModel):
    access: str
    type: str = 'bearer'
