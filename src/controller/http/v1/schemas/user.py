from pydantic import BaseModel, EmailStr

from src.core.components.user.domain.value_object import LanguageType, ThemeType


class RegisterUserSchema(BaseModel):
    email: EmailStr
    name: str
    password: str

    settings: RegisterSettingsSchema


class RegisterSettingsSchema(BaseModel):
    language: LanguageType
    theme: ThemeType


class ConfirmUserSchema(BaseModel):
    confirmation_code: str
