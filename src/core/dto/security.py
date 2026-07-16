from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JWTTokenDTO:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True)
class TokenPayload:
    user_id: int
    exp: str
