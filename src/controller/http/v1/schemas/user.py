from pydantic import BaseModel, EmailStr


class RegisterUserSchema(BaseModel):
    email: EmailStr
    name: str
    password: str


class ConfirmUserSchema(BaseModel):
    confirmation_code: str
