from dataclasses import dataclass


@dataclass(slots=True)
class JWTTokenDTO:
    access_token: str
    refresh_token: str


@dataclass(slots=True)
class TokenPayload:
    user_id: int
    exp: str
