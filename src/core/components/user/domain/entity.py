from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from src.core.components.user.domain.value_object import Language, RegistrationTokenType, Theme, UserRole


@dataclass(slots=True, frozen=True)
class UserDM:
    id: UUID
    email: str
    role: UserRole
    name: str
    hashed_password: str
    is_confirmed: bool
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def create(
        cls,
        ident: UUID,
        email: str,
        role: UserRole,
        name: str,
        hashed_pwd: str,
    ) -> Self:
        return cls(
            id=ident,
            email=email,
            role=role,
            name=name,
            hashed_password=hashed_pwd,
            is_confirmed=False,
            created_at=datetime.now(tz=UTC),
            updated_at=None,
        )


@dataclass(slots=True, frozen=True)
class SettingsDM:
    id: UUID
    language: Language
    theme: Theme

    user_id: UUID

    @classmethod
    def create(cls, ident: UUID, language: Language, theme: Theme, user_id: UUID) -> Self:
        return cls(
            id=ident,
            language=language,
            theme=theme,
            user_id=user_id,
        )


@dataclass(slots=True, frozen=True)
class RoleDM:
    id: int
    name: str
    description: str | None


@dataclass(slots=True, frozen=True)
class PermissionDM:
    id: int
    name: str
    description: str | None


@dataclass(slots=True, frozen=True)
class RegistrationTokenDM:
    id: UUID
    token_hash: str
    type: RegistrationTokenType
    is_active: bool
    expires_at: datetime
    created_at: datetime

    user_id: UUID

    @classmethod
    def create(
        cls,
        ident: UUID,
        token_hash: str,
        token_type: RegistrationTokenType,
        expires_at: datetime,
        user_id: UUID,
    ) -> Self:
        return cls(
            id=ident,
            token_hash=token_hash,
            type=token_type,
            is_active=True,
            expires_at=expires_at,
            created_at=datetime.now(tz=UTC),
            user_id=user_id,
        )
