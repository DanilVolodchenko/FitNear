from datetime import datetime
from enum import StrEnum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.models.base import Base


class RegistrationTokenType(StrEnum):
    EMAIL_CONFIRMATION = 'email_confirmation'
    PASSWORD_RESET = 'password_reset'  # noqa: S105


class RegistrationToken(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token_hash: Mapped[str]
    used_at: Mapped[datetime | None] = mapped_column(nullable=True, default=None)
    type: Mapped[RegistrationTokenType]
    attempts: Mapped[int] = mapped_column(default=0)
    expires_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class AuthTokenType(StrEnum):
    REFRESH = 'refresh'


class AuthToken(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    type: Mapped[AuthTokenType]
    expiration_date: Mapped[datetime]
    hash_token: Mapped[str]
    user_agent: Mapped[str | None]
    ip_address: Mapped[str | None]
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
