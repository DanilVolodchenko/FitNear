from pydantic import BaseModel


class LoginUserSchema(BaseModel):
    username: str
    password: str


class RegisterUserSchema(BaseModel):
    username: str
    name: str
    password: str
