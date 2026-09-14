from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text

from src.core.components.user.application.dto import CreateRegisterTokenDTO, CreateSettingsDTO, CreateUserDTO
from src.core.components.user.application.interface import (
    IRegistrationTokenEditor,
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
    ISettingsSaver,
    IUserEditor,
    IUserReader,
    IUserRemover,
    IUserSaver,
)
from src.core.components.user.domain.entity import RegistrationTokenDM, SettingsDM, UserDM


class UserRepository(IUserReader, IUserSaver, IUserEditor, IUserRemover):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, ident: int) -> UserDM | None:
        stmt = text('SELECT * FROM users WHERE id = :id')

        result = await self._session.execute(
            statement=stmt,
            params={'id': ident},
        )
        entity = result.mappings().one_or_none()

        if not entity:
            return None

        return UserDM(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            hashed_password=entity.hashed_password,
            is_confirmed=entity.is_confirmed,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def get_by_email(self, email: str) -> UserDM | None:
        stmt = text('SELECT * FROM users WHERE email = :email')

        result = await self._session.execute(
            statement=stmt,
            params={'email': email},
        )
        entity = result.mappings().one_or_none()

        if not entity:
            return None

        return UserDM(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            hashed_password=entity.hashed_password,
            is_confirmed=entity.is_confirmed,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, user_dto: CreateUserDTO) -> UserDM:
        stmt = text(
            """
            INSERT INTO users (email, name, hashed_password, is_confirmed)
            VALUES (:email, :name, :hashed_password, :is_confirmed)
            RETURNING *;
            """  # ruff: ignore[missing-trailing-comma]
        )

        result = await self._session.execute(
            statement=stmt,
            params={
                'email': user_dto.email,
                'name': user_dto.name,
                'hashed_password': user_dto.hashed_password,
                'is_confirmed': user_dto.is_confirmed,
            },
        )

        entity = result.mappings().one()

        return UserDM(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            hashed_password=entity.hashed_password,
            is_confirmed=entity.is_confirmed,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def confirm_user_email(self, user_id: int) -> None:
        stmt = text('UPDATE users SET is_confirmed = true WHERE id = :id')

        await self._session.execute(
            statement=stmt,
            params={'id': user_id},
        )

    async def remove_by_email(self, email: str) -> None:
        stmt = text('DELETE FROM users WHERE email = :email')

        await self._session.execute(statement=stmt, params={'email': email})


class SettingsRepository(ISettingsSaver):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, settings_dto: CreateSettingsDTO) -> SettingsDM:
        stmt = text('INSERT INTO settings (language, theme, user_id) VALUES (:language, :theme, :user_id) RETURNING *')

        result = await self._session.execute(
            statement=stmt,
            params={
                'language': settings_dto.language,
                'theme': settings_dto.theme,
                'user_id': settings_dto.user_id,
            },
        )

        entity = result.mappings().one()

        return SettingsDM(id=entity.id, language=entity.language, theme=entity.theme, user_id=entity.user_id)


class RegistrationTokenRepository(IRegistrationTokenReader, IRegistrationTokenSaver, IRegistrationTokenEditor):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_token_hash(self, token_hash: str) -> RegistrationTokenDM | None:
        stmt = text('SELECT * FROM registration_tokens WHERE token_hash = :token_hash')

        result = await self._session.execute(statement=stmt, params={'token_hash': token_hash})

        entity = result.mappings().one_or_none()

        if not entity:
            return None

        return RegistrationTokenDM(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            type=entity.type,
            is_active=entity.is_active,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )

    async def get_by_id(self, ident: int) -> RegistrationTokenDM | None:
        stmt = text('SELECT * FROM registration_tokens WHERE id = :id')
        result = await self._session.execute(statement=stmt, params={'id': ident})

        entity = result.mappings().one_or_none()

        if not entity:
            return None

        return RegistrationTokenDM(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            type=entity.type,
            is_active=entity.is_active,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )

    async def create(self, token_dto: CreateRegisterTokenDTO) -> RegistrationTokenDM:
        stmt = text(
            """
            INSERT INTO registration_tokens (user_id, token_hash, type, attempts, is_active, expires_at)
            VALUES (:user_id, :token_hash, :type, :attempts, :is_active, :expires_at)
            RETURNING *
            """  # ruff: ignore[missing-trailing-comma]
        )

        result = await self._session.execute(
            statement=stmt,
            params={
                'user_id': token_dto.user_id,
                'token_hash': token_dto.token_hash,
                'type': token_dto.type,
                'attempts': token_dto.attempts,
                'is_active': token_dto.is_active,
                'expires_at': token_dto.expires_at,
            },
        )

        entity = result.mappings().one()

        return RegistrationTokenDM(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            type=entity.type,
            is_active=entity.is_active,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )

    async def deactivate(self, token_id: int) -> None:
        stmt = text('UPDATE registration_tokens SET is_active = false WHERE id = :id')

        await self._session.execute(statement=stmt, params={'id': token_id})
