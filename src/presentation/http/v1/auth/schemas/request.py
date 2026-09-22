from pydantic import BaseModel, EmailStr

from src.core.components.user.domain.value_object import Language, Theme


class BaseAuthRequest(BaseModel):
    email: EmailStr


class RegisterUserRequest(BaseAuthRequest):
    name: str
    password: str

    settings: RegisterSettingsRequest


class LoginUserRequest(BaseAuthRequest):
    password: str


class RegisterSettingsRequest(BaseModel):
    language: Language
    theme: Theme


class ConfirmUserRequest(BaseModel):
    confirmation_code: str
