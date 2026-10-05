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
from src.core.components.user.domain.entity import RegistrationTokenDM, SettingsDM, UserDM
from src.core.components.user.domain.value_object import RegistrationTokenType
from src.core.exceptions.app_logic import (
    ConfirmationCodeError,
    CredentialsError,
    FoundError,
    NotFoundError,
    TokenExpiredError,
)
from src.core.shared_kernel.application.interfaces.token import IAuthTokenSaver
from src.core.shared_kernel.application.interfaces.event_bus import IEventBus
from src.core.shared_kernel.application.interfaces.generator import IStringGenerator, IUUIDGenerator
from src.core.shared_kernel.application.interfaces.security import IHasher, IJWTToken, IPwdHasher
from src.core.shared_kernel.application.interfaces.transaction import ITransactionManager
from src.core.shared_kernel.domain.entity import AuthTokenDM
from src.core.shared_kernel.domain.value_object import AuthTokenType
from src.infrastructure.models.value_object import UserRole


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
        self._reg_token_saver = reg_token_saver
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
                raise FoundError('User already exists')

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

        registration_code = self._string_generator.generate(EMAIL_CONFIRMATION_CODE_LENGTH)
        token_hash = await self._hasher.hash(registration_code, self._security_config.hash_key)

        expires_at = datetime.now(tz=UTC) + timedelta(seconds=EMAIL_CONFIRMATION_TOKEN_EXP_TIME_SEC)

        reg_token_id = self._uuid_generator.generate()
        reg_token_dm = RegistrationTokenDM.create(
            ident=reg_token_id,
            token_hash=token_hash,
            token_type=RegistrationTokenType.EMAIL_CONFIRMATION,
            expires_at=expires_at,
            user_id=user_id,
        )

        await self._user_saver.save(user_dm)
        await self._settings_saver.save(settings_dm)
        await self._reg_token_saver.save(reg_token_dm)

        await self._trx_manager.commit()

        await self._event_bus.publish(
            UserEmailConfirmationEvent(
                subject='Регистрация',
                sender=self._server_config.email,
                recipient=user_dm.email,
                content=f'Код подтверждения: {registration_code}',
            ),
        )

        return RegisteredUserDTO(registration_id=reg_token_dm.id, expires_at=reg_token_dm.expires_at)


class ConfirmUserService:
    def __init__(
        self,
        config: Config,
        user_editor: IUserEditor,
        reg_token_reader: IRegistrationTokenReader,
        reg_token_editor: IRegistrationTokenEditor,
        hasher: IHasher,
        trx_manager: ITransactionManager,
    ) -> None:
        self._config = config
        self._user_editor = user_editor
        self._reg_token_reader = reg_token_reader
        self._reg_token_editor = reg_token_editor
        self._hasher = hasher
        self._trx_manager = trx_manager

    async def __call__(self, registration_id: UUID, confirm_user_dto: ConfirmUserDTO) -> None:

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
        pwd_hasher: IPwdHasher,
        uuid4_generator: IUUIDGenerator,
        uuid7_generator: IUUIDGenerator,
        jwt_token: IJWTToken,
        hasher: IHasher,
        auth_token_saver: IAuthTokenSaver,
        trx_manager: ITransactionManager,
    ) -> None:
        self._security_config = security_config
        self._user_reader = user_reader
        self._pwd_hasher = pwd_hasher
        self._uuid4_generator = uuid4_generator
        self._uuid7_generator = uuid7_generator
        self._jwt_token = jwt_token
        self._hasher = hasher
        self._auth_token_saver = auth_token_saver
        self._trx_manager = trx_manager

    async def __call__(self, login_user_dto: LoginUserDTO) -> JWTTokenDTO:
        user_dm = await self._user_reader.get_by_email(login_user_dto.email)

        if not user_dm or not user_dm.is_confirmed:
            raise CredentialsError('Invalid credentials')

        if not await self._pwd_hasher.verify(user_dm.hashed_password, login_user_dto.password):
            raise CredentialsError('Invalid credentials')

        current_time = datetime.now(tz=UTC)

        access_token, access_token_dm = await self._create_token(
            user_dm,
            AuthTokenType.ACCESS,
            ip_address=login_user_dto.ip_address,
            user_agent=login_user_dto.user_agent,
            expires_at=current_time + timedelta(seconds=ACCESS_TOKEN_EXP_TIME_SEC),
            issued_at=current_time,
        )
        refresh_token, refresh_token_dm = await self._create_token(
            user_dm,
            AuthTokenType.REFRESH,
            ip_address=login_user_dto.ip_address,
            user_agent=login_user_dto.user_agent,
            expires_at=current_time + timedelta(seconds=REFRESH_TOKEN_EXP_TIME_SEC),
            issued_at=current_time,
        )

        await self._auth_token_saver.add(access_token_dm)
        await self._auth_token_saver.add(refresh_token_dm)

        await self._trx_manager.commit()

        return JWTTokenDTO(access=access_token, refresh=refresh_token)

    async def _create_token(
        self,
        user_dm: UserDM,
        token_type: AuthTokenType,
        *,
        ip_address: str | None,
        user_agent: str | None,
        expires_at: datetime,
        issued_at: datetime,
    ) -> tuple[str, AuthTokenDM]:

        auth_token_id = self._uuid7_generator.generate()

        payload = {
            'sub': str(user_dm.id),
            'role': user_dm.role,
            'type': token_type,
            'exp': expires_at,
            'iat': issued_at,
            'jti': str(auth_token_id),
        }

        jwt_token = await self._jwt_token.encode(
            payload,
            secret_key=self._security_config.jwt_secret_key,
            algorithm=self._security_config.jwt_algorithm,
        )

        auth_token_hash = await self._hasher.hash(jwt_token, self._security_config.hash_key)
        auth_token_dm = AuthTokenDM.create(
            ident=auth_token_id,
            token_type=token_type,
            token_hash=auth_token_hash,
            user_agent=user_agent,
            ip_address=ip_address,
            family_id=None,
            expires_at=expires_at,
            user_id=user_dm.id,
        )

        return jwt_token, auth_token_dm


class LogoutUserService:
    async def __call__(self) -> None: ...
