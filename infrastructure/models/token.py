from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from domain.value_objects.token_type import AuthTokenType, RegistrationTokenType
from infrastructure.models.base import Base


class RegistrationToken(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token_hash: Mapped[str] = mapped_column(index=True)
    used_at: Mapped[datetime | None] = mapped_column(default=None, nullable=True)
    type: Mapped[RegistrationTokenType]
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    expires_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class AuthToken(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    type: Mapped[AuthTokenType]
    token_hash: Mapped[str] = mapped_column(index=True)
    user_agent: Mapped[str | None]
    ip_address: Mapped[str | None]
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
