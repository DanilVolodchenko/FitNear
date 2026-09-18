from datetime import UTC, datetime, timedelta

from config import Config, SecurityConfig, ServerConfig
from src.core.components.user.application.constants import (
    ACCESS_TOKEN_EXP_TIME_SEC,
    EMAIL_CONFIRMATION_CODE_LENGTH,
    EMAIL_CONFIRMATION_TOKEN_EXP_TIME_SEC,
    REFRESH_TOKEN_EXP_TIME_SEC,
)
from src.core.components.user.application.dto import (
    ConfirmUserDTO,
    CreateRegisterTokenDTO,
    CreateSettingsDTO,
    CreateUserDTO,
    JWTTokenDTO,
    LoginUserDTO,
    RegisteredUserDTO,
    RegisterUserDTO,
)
from src.core.components.user.application.event import UserEmailConfirmationEvent
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
from src.core.components.user.domain.value_object import AuthTokenType, RegistrationTokenType
from src.core.exceptions.app_logic import ConfirmationCodeError, FoundError, NotFoundError, TokenExpiredError
from src.core.shared_kernel.application.interfaces.event_bus import IEventBus
from src.core.shared_kernel.application.interfaces.generator import IStringGenerator, IUUIDGenerator
from src.core.shared_kernel.application.interfaces.security import IHasher, IJWTToken, IPwdHasher
from src.core.shared_kernel.application.interfaces.transaction import ITransactionManager


class RegisterUserService:
    def __init__(
        self,
        security_config: SecurityConfig,
        server_config: ServerConfig,
        user_reader: IUserReader,
        user_saver: IUserSaver,
        user_remover: IUserRemover,
        settings_saver: ISettingsSaver,
        reg_token_saver: IRegistrationTokenSaver,
        pwd_hasher: IPwdHasher,
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
        self._reg_token_saver = reg_token_saver
        self._pwd_hasher = pwd_hasher
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
                raise FoundError('User already exists')

        hashed_pwd = await self._pwd_hasher.hash(reg_user_dto.password)

        user_dm = await self._user_saver.create(
            CreateUserDTO(
                email=reg_user_dto.email,
                name=reg_user_dto.name,
                hashed_password=hashed_pwd,
                is_confirmed=False,
            ),
        )

        await self._settings_saver.create(
            CreateSettingsDTO(
                language=reg_user_dto.settings.language,
                theme=reg_user_dto.settings.theme,
                user_id=user_dm.id,
            ),
        )

        registration_code = await self._string_generator(EMAIL_CONFIRMATION_CODE_LENGTH)

        token_hash = await self._hasher.hash(registration_code, self._security_config.hash_key)

        expires_at = datetime.now(tz=UTC) + timedelta(seconds=EMAIL_CONFIRMATION_TOKEN_EXP_TIME_SEC)

        reg_token = await self._reg_token_saver.create(
            CreateRegisterTokenDTO(
                user_id=user_dm.id,
                token_hash=token_hash,
                type=RegistrationTokenType.EMAIL_CONFIRMATION,
                expires_at=expires_at,
            ),
        )

        await self._trx_manager.commit()

        from loguru import logger

        logger.success(registration_code)

        await self._event_bus.publish(
            UserEmailConfirmationEvent(
                subject='Регистрация',
                sender=self._server_config.email,
                recipient=user_dm.email,
                content=f'Код подтверждения: {registration_code}',
            ),
        )

        return RegisteredUserDTO(registration_id=reg_token.id, expires_at=reg_token.expires_at)


class ConfirmUserService:
    def __init__(
        self,
        config: Config,
        user_reader: IUserReader,
        user_editor: IUserEditor,
        reg_token_reader: IRegistrationTokenReader,
        reg_token_editor: IRegistrationTokenEditor,
        hasher: IHasher,
        trx_manager: ITransactionManager,
    ) -> None:
        self._config = config
        self._user_reader = user_reader
        self._user_editor = user_editor
        self._reg_token_reader = reg_token_reader
        self._reg_token_editor = reg_token_editor
        self._hasher = hasher
        self._trx_manager = trx_manager

    async def __call__(self, registration_id: int, confirm_user_dto: ConfirmUserDTO) -> None:

        registration_token_dm = await self._reg_token_reader.get_by_id(registration_id)

        if not registration_token_dm:
            raise NotFoundError('Registration token not found')

        if not registration_token_dm.is_active:
            raise NotFoundError('Registration token already used')

        if registration_token_dm.expires_at < datetime.now(tz=UTC):
            raise TokenExpiredError('Code has expired')

        hash_code = await self._hasher.hash(confirm_user_dto.confirmation_code, self._config.security.hash_key)

        is_correct_code = await self._hasher.compare(hash_code, registration_token_dm.token_hash)

        if not is_correct_code:
            raise ConfirmationCodeError('Incorrect confirmation code')

        await self._user_editor.confirm_user_email(registration_token_dm.user_id)
        await self._reg_token_editor.deactivate(registration_token_dm.id)

        await self._trx_manager.commit()


class LoginUserService:
    def __init__(
        self,
        security_config: SecurityConfig,
        user_reader: IUserReader,
        uuid_generator: IUUIDGenerator,
        jwt_token: IJWTToken,
        hasher: IHasher,
    ) -> None:
        self._security_config = security_config
        self._user_reader = user_reader
        self._uuid_generator = uuid_generator
        self._jwt_token = jwt_token
        self._hasher = hasher

    async def __call__(self, login_user_dto: LoginUserDTO) -> JWTTokenDTO:
        user_dm = await self._user_reader.get_by_email(login_user_dto.email)

        if not user_dm or not user_dm.is_confirmed:
            raise NotFoundError('User not found')

        current_time = datetime.now(tz=UTC)

        access_token_expires_at = current_time + timedelta(seconds=ACCESS_TOKEN_EXP_TIME_SEC)
        refresh_token_expires_at = current_time + timedelta(seconds=REFRESH_TOKEN_EXP_TIME_SEC)

        access_token_jti = await self._uuid_generator()
        refresh_token_jti = await self._uuid_generator()

        access_payload = {
            'sub': user_dm.id,
            'role': user_dm.role,
            'type': AuthTokenType.ACCESS,
            'exp': access_token_expires_at,
            'iat': current_time,
            'jti': str(access_token_jti),
        }
        refresh_payload = {
            'sub': user_dm.id,
            'role': user_dm.role,
            'type': AuthTokenType.ACCESS,
            'exp': refresh_token_expires_at,
            'iat': current_time,
            'jti': str(refresh_token_jti),
        }

        access_token = await self._jwt_token.encode(
            access_payload,
            secret_key=self._security_config.jwt_secret_key,
            algorithm=self._security_config.jwt_algorithm,
        )
        refresh_token = await self._jwt_token.encode(
            refresh_payload,
            secret_key=self._security_config.jwt_secret_key,
            algorithm=self._security_config.jwt_algorithm,
        )

        return JWTTokenDTO(access=access_token, refresh=refresh_token)


class LogoutUserService:
    async def __call__(self): ...
