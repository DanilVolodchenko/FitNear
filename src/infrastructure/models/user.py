from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.models.base import Base
from src.infrastructure.models.utils import get_enum_values
from src.infrastructure.models.value_object import Language, Theme, UserRole

users_roles = Table(
    'users_roles',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', sa.UUID, ForeignKey('users.id', ondelete='CASCADE')),
    Column('role_id', sa.UUID, ForeignKey('roles.id', ondelete='CASCADE')),
    UniqueConstraint('user_id', 'role_id'),
)

users_permissions = Table(
    'users_permissions',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', sa.UUID, ForeignKey('users.id', ondelete='CASCADE')),
    Column('permission_id', sa.UUID, ForeignKey('permissions.id', ondelete='CASCADE')),
    UniqueConstraint('user_id', 'permission_id'),
)

roles_permissions = Table(
    'roles_permissions',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('role_id', sa.UUID, ForeignKey('roles.id', ondelete='CASCADE')),
    Column('permission_id', sa.UUID, ForeignKey('permissions.id', ondelete='CASCADE')),
    UniqueConstraint('role_id', 'permission_id'),
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        sa.Enum(UserRole, name='user_role_enum', values_callable=get_enum_values),
        default=UserRole.CLIENT,
        nullable=False,
    )
    is_confirmed: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, onupdate=func.now())

    settings: Mapped[Settings] = relationship(back_populates='user', uselist=False)
    roles: Mapped[list[Role]] = relationship(secondary=users_roles, back_populates='users')
    permissions: Mapped[list[Permission]] = relationship(secondary=users_permissions, back_populates='users')


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=True, default=None)

    users: Mapped[list[User]] = relationship(secondary=users_roles, back_populates='roles')
    permissions: Mapped[list[Permission]] = relationship(secondary=roles_permissions, back_populates='roles')


class Permission(Base):
    __tablename__ = 'permissions'

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=True, default=None)

    users: Mapped[list[User]] = relationship(secondary=users_permissions, back_populates='permissions')
    roles: Mapped[list[Role]] = relationship(secondary=roles_permissions, back_populates='permissions')


class Settings(Base):
    __tablename__ = 'settings'

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    language: Mapped[Language] = mapped_column(
        sa.Enum(Language, name='settings_language_enum', values_callable=get_enum_values),
        default=Language.RU,
        nullable=False,
    )
    theme: Mapped[Theme] = mapped_column(
        sa.Enum(Theme, name='settings_theme_enum', values_callable=get_enum_values),
        default=Theme.SYSTEM,
        nullable=False,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True,
        unique=True,
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates='settings', single_parent=True)
