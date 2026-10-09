import contextlib
from datetime import UTC, datetime, timedelta
from uuid import UUID

from config import Config, SecurityConfig, ServerConfig
from src.core.components.user.application.constants import (
    ACCESS_TOKEN_EXP_TIME_SEC,
    EMAIL_CONFIRMATION_CODE_LENGTH,
    EMAIL_CONFIRMATION_TOKEN_EXP_TIME_SEC,
    REFRESH_TOKEN_EXP_TIME_SEC,
)
from src.core.components.user.application.dto import (
    ConfirmUserDTO,
    JWTTokenDTO,
    LoginUserDTO,
    LogoutUserDTO,
    RegisteredUserDTO,
    RegisterUserDTO,
)
from src.core.components.user.application.event import UserEmailConfirmationEvent
from src.core.components.user.application.exception import RegistrationTokenError, UserError
from src.core.components.user.application.interface import (
    IConfirmationCodeEditor,
    IConfirmationCodeReader,
    IConfirmationCodeSaver,
    ISettingsSaver,
    IUserEditor,
    IUserReader,
    IUserRemover,
    IUserSaver,
)
from src.core.components.user.domain.entity import ConfirmationCodeDM, SettingsDM, UserDM
from src.core.components.user.domain.value_object import ConfirmationCodeType
from src.core.shared_kernel.application.dto.security import JWTPayloadDTO
from src.core.shared_kernel.application.exceptions.security import JWTError
from src.core.shared_kernel.application.interfaces.event_bus import IEventBus
from src.core.shared_kernel.application.interfaces.generator import IStringGenerator, IUUIDGenerator
from src.core.shared_kernel.application.interfaces.security import IHasher, IJWTToken, IPwdHasher
from src.core.shared_kernel.application.interfaces.token import (
    IRefreshTokenEditor,
    IRefreshTokenReader,
    IRefreshTokenSaver,
)
from src.core.shared_kernel.application.interfaces.transaction import ITransactionManager
from src.core.shared_kernel.domain.entity import RefreshTokenDM
from src.core.shared_kernel.domain.value_object import JWTTokenType, UserRole


class RegisterUserService:
    def __init__(
        self,
        security_config: SecurityConfig,
        server_config: ServerConfig,
        user_reader: IUserReader,
        user_saver: IUserSaver,
        user_remover: IUserRemover,
        settings_saver: ISettingsSaver,
        confirmation_code_saver: IConfirmationCodeSaver,
        pwd_hasher: IPwdHasher,
        uuid_generator: IUUIDGenerator,
        string_generator: IStringGenerator,
        hasher: IHasher,
        trx_manager: ITransactionManager,
        event_bus: IEventBus,
    ) -> None:
        self._security_config = security_config
        self._server_config = server_config
        self._user_reader = user_reader
        self._user_saver = user_saver
        self._user_remover = user_remover
        self._settings_saver = settings_saver
        self._confirmation_code_saver = confirmation_code_saver
        self._pwd_hasher = pwd_hasher
        self._uuid_generator = uuid_generator
        self._string_generator = string_generator
        self._hasher = hasher
        self._trx_manager = trx_manager
        self._event_bus = event_bus

    async def __call__(self, reg_user_dto: RegisterUserDTO) -> RegisteredUserDTO:
        user_dm = await self._user_reader.get_by_email(reg_user_dto.email)

        if user_dm:
            if not user_dm.is_confirmed:
                await self._user_remover.remove_by_email(user_dm.email)

            else:
                raise UserError('User already exists')

        hashed_pwd = await self._pwd_hasher.hash(reg_user_dto.password)

        user_id = self._uuid_generator.generate()
        user_dm = UserDM.create(
            ident=user_id,
            email=reg_user_dto.email,
            role=UserRole.CLIENT,
            name=reg_user_dto.name,
            hashed_pwd=hashed_pwd,
        )

        settings_id = self._uuid_generator.generate()
        settings_dm = SettingsDM.create(
            ident=settings_id,
            language=reg_user_dto.settings.language,
            theme=reg_user_dto.settings.theme,
            user_id=user_id,
        )

        confirmation_code = self._string_generator.generate(EMAIL_CONFIRMATION_CODE_LENGTH)
        code_hash = await self._hasher.hash(confirmation_code, self._security_config.hash_key)

        expires_at = datetime.now(tz=UTC) + timedelta(seconds=EMAIL_CONFIRMATION_TOKEN_EXP_TIME_SEC)

        confirmation_code_id = self._uuid_generator.generate()
        confirmation_code_dm = ConfirmationCodeDM.create(
            ident=confirmation_code_id,
            code_hash=code_hash,
            code_type=ConfirmationCodeType.EMAIL,
            expires_at=expires_at,
            user_id=user_id,
        )

        await self._user_saver.save(user_dm)
        await self._settings_saver.save(settings_dm)
        await self._confirmation_code_saver.save(confirmation_code_dm)

        await self._trx_manager.commit()

        await self._event_bus.publish(
            UserEmailConfirmationEvent(
                subject='Регистрация',
                sender=self._server_config.email,
                recipient=user_dm.email,
                content=f'Код подтверждения: {confirmation_code}',
            ),
        )

        return RegisteredUserDTO(registration_id=confirmation_code_dm.id, expires_at=confirmation_code_dm.expires_at)


class ConfirmUserService:
    def __init__(
        self,
        config: Config,
        user_editor: IUserEditor,
        confirmation_code_reader: IConfirmationCodeReader,
        confirmation_code_editor: IConfirmationCodeEditor,
        hasher: IHasher,
        trx_manager: ITransactionManager,
    ) -> None:
        self._config = config
        self._user_editor = user_editor
        self._confirmation_code_reader = confirmation_code_reader
        self._confirmation_code_editor = confirmation_code_editor
        self._hasher = hasher
        self._trx_manager = trx_manager

    async def __call__(self, registration_id: UUID, confirm_user_dto: ConfirmUserDTO) -> None:

        registration_token_dm = await self._confirmation_code_reader.get_by_id(registration_id)

        if not registration_token_dm:
            raise RegistrationTokenError('Registration token not found')

        if not registration_token_dm.is_active:
            raise RegistrationTokenError('Registration token already used')

        if registration_token_dm.expires_at < datetime.now(tz=UTC):
            raise RegistrationTokenError('Registration code has expired')

        hash_code = await self._hasher.hash(confirm_user_dto.confirmation_code, self._config.security.hash_key)

        is_correct_code = await self._hasher.compare(hash_code, registration_token_dm.code_hash)

        if not is_correct_code:
            raise RegistrationTokenError('Incorrect registration code')

        await self._user_editor.confirm_user_email(registration_token_dm.user_id)
        await self._confirmation_code_editor.deactivate(registration_token_dm.id)

        await self._trx_manager.commit()


class LoginUserService:
    def __init__(
        self,
        security_config: SecurityConfig,
        user_reader: IUserReader,
        pwd_hasher: IPwdHasher,
        uuid4_generator: IUUIDGenerator,
        uuid7_generator: IUUIDGenerator,
        jwt_token: IJWTToken,
        hasher: IHasher,
        refresh_token_saver: IRefreshTokenSaver,
        trx_manager: ITransactionManager,
    ) -> None:
        self._security_config = security_config
        self._user_reader = user_reader
        self._pwd_hasher = pwd_hasher
        self._uuid4_generator = uuid4_generator
        self._uuid7_generator = uuid7_generator
        self._jwt_token = jwt_token
        self._hasher = hasher
        self._refresh_token_saver = refresh_token_saver
        self._trx_manager = trx_manager

    async def __call__(self, login_user_dto: LoginUserDTO) -> JWTTokenDTO:
        user_dm = await self._user_reader.get_by_email(login_user_dto.email)

        if not user_dm or not user_dm.is_confirmed:
            raise UserError('Invalid credentials')

        if not await self._pwd_hasher.verify(user_dm.hashed_password, login_user_dto.password):
            raise UserError('Invalid credentials')

        current_time = datetime.now(tz=UTC)

        access_token_id = self._uuid7_generator.generate()
        access_token_expires_at = current_time + timedelta(seconds=ACCESS_TOKEN_EXP_TIME_SEC)

        access_jwt_token = await self._create_jwt_token(
            user_dm,
            access_token_id,
            JWTTokenType.ACCESS,
            expires_at=access_token_expires_at,
            issued_at=current_time,
        )

        refresh_token_id = self._uuid7_generator.generate()
        refresh_token_expires_at = current_time + timedelta(seconds=REFRESH_TOKEN_EXP_TIME_SEC)

        refresh_jwt_token = await self._create_jwt_token(
            user_dm,
            refresh_token_id,
            JWTTokenType.REFRESH,
            expires_at=refresh_token_expires_at,
            issued_at=current_time,
        )

        auth_token_hash = await self._hasher.hash(refresh_jwt_token, self._security_config.hash_key)
        refresh_token_dm = RefreshTokenDM.create(
            ident=refresh_token_id,
            token_hash=auth_token_hash,
            user_agent=login_user_dto.user_agent,
            ip_address=login_user_dto.ip_address,
            family_id=None,
            expires_at=refresh_token_expires_at,
            user_id=user_dm.id,
        )

        from loguru import logger
        logger.success(refresh_jwt_token)

        await self._refresh_token_saver.add(refresh_token_dm)

        await self._trx_manager.commit()

        return JWTTokenDTO(access_token=access_jwt_token, refresh_token=refresh_jwt_token)

    async def _create_jwt_token(
        self,
        user_dm: UserDM,
        token_id: UUID,
        token_type: JWTTokenType,
        *,
        expires_at: datetime,
        issued_at: datetime,
    ) -> str:

        payload = JWTPayloadDTO(
            jti=token_id,
            sub=user_dm.id,
            role=user_dm.role,
            type=token_type,
            exp=expires_at,
            iat=issued_at,
        )

        jwt_token = await self._jwt_token.encode(
            payload.to_dict(),
            secret_key=self._security_config.jwt_secret_key,
            algorithm=self._security_config.jwt_encode_algorithm,
        )

        return jwt_token


class LogoutUserService:
    def __init__(
        self,
        security_config: SecurityConfig,
        refresh_token_reader: IRefreshTokenReader,
        refresh_token_editor: IRefreshTokenEditor,
        jwt_token: IJWTToken,
        trx_manager: ITransactionManager,
    ) -> None:
        self._security_config = security_config
        self._refresh_token_reader = refresh_token_reader
        self._refresh_token_editor = refresh_token_editor
        self._jwt_token = jwt_token
        self._trx_manager = trx_manager

    async def __call__(self, logout_user_dto: LogoutUserDTO) -> None:
        from loguru import logger
        logger.success(logout_user_dto)
        if logout_user_dto.refresh_token:
            with contextlib.suppress(JWTError):
                await self._deactivate_token(logout_user_dto.refresh_token)

        await self._trx_manager.commit()

    async def _deactivate_token(self, token: str) -> None:
        """Decode and deactivate token."""

        raw_payload = await self._jwt_token.decode(
            token,
            self._security_config.jwt_secret_key,
            self._security_config.jwt_decode_algorithms,
        )

        jwt_payload = JWTPayloadDTO.from_dict(raw_payload)

        auth_token_dm = await self._refresh_token_reader.get_by_id(jwt_payload.jti)

        if auth_token_dm and auth_token_dm.is_active:
            await self._refresh_token_editor.deactivate_by_id(jwt_payload.jti)
