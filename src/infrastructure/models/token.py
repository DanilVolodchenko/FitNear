from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.components.user.domain.value_object import ConfirmationCodeType
from src.infrastructure.models.base import Base
from src.infrastructure.models.utils import get_enum_values


class ConfirmationCode(Base):
    __tablename__ = 'confirmation_codes'

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    code_hash: Mapped[str] = mapped_column(index=True)
    used_at: Mapped[datetime | None] = mapped_column(default=None, nullable=True)
    type: Mapped[ConfirmationCodeType] = mapped_column(
        sa.Enum(ConfirmationCodeType, name='confirmation_code_type_enum', values_callable=get_enum_values),
        nullable=False,
    )
    attempts: Mapped[int] = mapped_column(default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    token_hash: Mapped[str] = mapped_column(String(256), index=True)
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    family_id: Mapped[UUID | None] = mapped_column(sa.UUID, index=True, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
