from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.models.base import Base
from src.infrastructure.models.choices import AuthTokenType, RegistrationTokenType


class RegistrationToken(Base):
    __tablename__ = 'registration_tokens'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    token_hash: Mapped[str] = mapped_column(index=True)
    used_at: Mapped[datetime | None] = mapped_column(default=None, nullable=True)
    type: Mapped[RegistrationTokenType]
    attempts: Mapped[int] = mapped_column(default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AuthToken(Base):
    __tablename__ = 'auth_tokens'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    type: Mapped[AuthTokenType]
    token_hash: Mapped[str] = mapped_column(index=True)
    user_agent: Mapped[str | None]
    ip_address: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
