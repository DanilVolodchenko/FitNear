import dataclasses
from datetime import UTC, datetime
from typing import Any, Self
from uuid import UUID

from src.core.shared_kernel.domain.value_object import AuthTokenType, UserRole


@dataclasses.dataclass(frozen=True, slots=True)
class JWTPayloadDTO:
    jti: UUID
    sub: UUID
    role: UserRole
    type: AuthTokenType
    exp: datetime
    iat: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            'jti': str(self.jti),
            'sub': str(self.sub),
            'role': self.role.value,
            'type': self.type.value,
            'exp': self.exp.timestamp(),
            'iat': self.iat.timestamp(),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> Self:
        return cls(
            jti=UUID(payload['jti']),
            sub=UUID(payload['sub']),
            role=UserRole(payload['role']),
            type=AuthTokenType(payload['type']),
            exp=datetime.fromtimestamp(payload['exp'], tz=UTC),
            iat=datetime.fromtimestamp(payload['iat'], tz=UTC),
        )
