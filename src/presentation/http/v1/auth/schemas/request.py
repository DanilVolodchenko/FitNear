from pydantic import BaseModel, EmailStr

from src.core.components.user.domain.value_object import Language, Theme


class BaseAuthRequest(BaseModel):
    email: EmailStr


class RegisterUserRequest(BaseAuthRequest):
    name: str
    password: str

    settings: RegisterSettingsRequest


class RegisterSettingsRequest(BaseModel):
    language: Language
    theme: Theme


class ConfirmUserRequest(BaseModel):
    confirmation_code: str


class LoginUserRequest(BaseAuthRequest):
    password: str


class LogoutUserRequest(BaseModel):
    access_token: str
    refresh_token: str
