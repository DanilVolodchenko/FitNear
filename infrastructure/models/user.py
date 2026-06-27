from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.models.base import Base

users_roles = Table(
    'users_roles',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id')),
    UniqueConstraint('user_id', 'role_id'),
)

roles_permissions = Table(
    'roles_permissions',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id')),
    UniqueConstraint('role_id', 'permission_id'),
)


class User(Base):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    roles: Mapped[list[Role]] = relationship(secondary=users_roles, back_populates='users')
    permissions: Mapped[list[Permission]] = relationship(secondary=users_roles, back_populates='users')


class Role(Base):
    name: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=True, default=None)

    users: Mapped[list[User]] = relationship(secondary=users_roles, back_populates='roles')


class Permission(Base):
    name: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=True, default=None)

    users: Mapped[list[User]] = relationship(secondary=users_roles, back_populates='permissions')
