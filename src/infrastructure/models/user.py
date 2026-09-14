from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.models.base import Base
from src.infrastructure.models.choices import LanguageType, ThemeType

users_roles = Table(
    'users_roles',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE')),
    UniqueConstraint('user_id', 'role_id'),
)

users_permissions = Table(
    'users_permissions',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE')),
    UniqueConstraint('user_id', 'permission_id'),
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
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_confirmed: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, onupdate=func.now())

    setting: Mapped[Settings] = relationship(back_populates='user', uselist=False)
    roles: Mapped[list[Role]] = relationship(secondary=users_roles, back_populates='users')
    permissions: Mapped[list[Permission]] = relationship(secondary=users_permissions, back_populates='users')


class Role(Base):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=True, default=None)

    users: Mapped[list[User]] = relationship(secondary=users_roles, back_populates='roles')
    permissions: Mapped[list[Permission]] = relationship(secondary=roles_permissions, back_populates='roles')


class Permission(Base):
    __tablename__ = 'permissions'

    name: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=True, default=None)

    users: Mapped[list[User]] = relationship(secondary=users_permissions, back_populates='permissions')
    roles: Mapped[list[Role]] = relationship(secondary=roles_permissions, back_populates='permissions')


class Settings(Base):
    __tablename__ = 'settings'

    language: Mapped[LanguageType]
    theme: Mapped[ThemeType]

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True,
        unique=True,
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates='setting', single_parent=True)
