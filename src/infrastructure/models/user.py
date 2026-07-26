from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.models.base import Base

users_roles = Table(
    'users_roles',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE')),
    UniqueConstraint('user_id', 'role_id'),
)

roles_permissions = Table(
    'roles_permissions',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE')),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE')),
    UniqueConstraint('role_id', 'permission_id'),
)


class User(Base):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]
    password: Mapped[str]
    is_confirmed: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # can user server_onupdate, but we need in trigger in db
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, onupdate=func.now())

    roles: Mapped[list[Role]] = relationship(secondary=users_roles, back_populates='users')


class Role(Base):
    name: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=True, default=None)

    users: Mapped[list[User]] = relationship(secondary=users_roles, back_populates='roles')
    permissions: Mapped[list[Permission]] = relationship(secondary=roles_permissions, back_populates='roles')


class Permission(Base):
    name: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=True, default=None)

    roles: Mapped[list[Permission]] = relationship(secondary=roles_permissions, back_populates='permissions')
