from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Uuid as SQLUuid
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.models.base import Base
from src.infrastructure.models.utils import get_enum_values
from src.infrastructure.models.value_object import AuthTokenType, RegistrationTokenType


class RegistrationToken(Base):
    __tablename__ = 'registration_tokens'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token_hash: Mapped[str] = mapped_column(index=True)
    used_at: Mapped[datetime | None] = mapped_column(default=None, nullable=True)
    type: Mapped[RegistrationTokenType] = mapped_column(
        SQLEnum(RegistrationTokenType, name='registration_token_type_enum', values_callable=get_enum_values),
        nullable=False,
    )
    attempts: Mapped[int] = mapped_column(default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))


class AuthToken(Base):
    __tablename__ = 'auth_tokens'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[AuthTokenType] = mapped_column(
        SQLEnum(AuthTokenType, name='auth_token_type_enum', values_callable=get_enum_values),
        nullable=False,
    )
    jti: Mapped[UUID] = mapped_column(SQLUuid, unique=True, index=True, nullable=False)
    token_hash: Mapped[str] = mapped_column(String(256), index=True)
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    family_id: Mapped[UUID | None] = mapped_column(SQLUuid, index=True, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
