from pydantic import BaseModel, EmailStr

from src.core.components.user.domain.value_object import LanguageType, ThemeType


class BaseUserSchema(BaseModel):
    email: EmailStr


class RegisterUserSchema(BaseUserSchema):
    name: str
    password: str

    settings: RegisterSettingsSchema


class LoginUserSchema(BaseUserSchema):
    password: str


class RegisterSettingsSchema(BaseModel):
    language: LanguageType
    theme: ThemeType


class ConfirmUserSchema(BaseModel):
    confirmation_code: str
