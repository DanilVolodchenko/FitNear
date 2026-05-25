from datetime import datetime
from enum import StrEnum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.models.base import Base


class TokenType(StrEnum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class AuthToken(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    type: Mapped[TokenType]
    expiration_date: Mapped[datetime]
    hash_token: Mapped[str]
    user_agent: Mapped[str | None]
    ip_address: Mapped[str | None]
    expired: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
