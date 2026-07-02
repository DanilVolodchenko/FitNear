from pydantic import BaseModel, EmailStr


class LoginUserSchema(BaseModel):
    username: str
    password: str


class RegisterUserSchema(BaseModel):
    email: EmailStr
    name: str
    password: str
