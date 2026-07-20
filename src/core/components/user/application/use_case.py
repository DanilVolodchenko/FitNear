from datetime import UTC, datetime, timedelta

from config import Config, SecurityConfig
from src.core.components.user.application.constants import (
    EMAIL_CONFIRMATION_CODE_LENGTH,
    EMAIL_CONFIRMATION_TOKEN_TIME_SEC,
)
from src.core.components.user.application.dto import ConfirmUserDTO, CreateRegisterTokenDTO, CreateUserDTO
from src.core.components.user.application.interface import (
    IRegistrationTokenEditor,
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
    IUserEditor,
    IUserReader,
    IUserRemover,
    IUserSaver,
)
from src.core.components.user.domain.entity import UserDM
from src.core.components.user.domain.value_object import RegistrationTokenType
from src.core.errors import FoundError
from src.core.interfaces.generator import IStringGenerator
from src.core.interfaces.security import IHasher, IPwdHasher
from src.core.interfaces.transaction import ITransactionManager


class RegisterUserUseCase:
    def __init__(
        self,
        security_config: SecurityConfig,
        user_reader: IUserReader,
        user_saver: IUserSaver,
        user_remover: IUserRemover,
        reg_token_saver: IRegistrationTokenSaver,
        pwd_hasher: IPwdHasher,
        string_generator: IStringGenerator,
        hasher: IHasher,
        trx_manager: ITransactionManager,
    ) -> None:
        self._security_config = security_config
        self._user_reader = user_reader
        self._user_saver = user_saver
        self._user_remover = user_remover
        self._reg_token_saver = reg_token_saver
        self._pwd_hasher = pwd_hasher
        self._string_generator = string_generator
        self._hasher = hasher
        self._trx_manager = trx_manager

    async def __call__(self, create_user_dto: CreateUserDTO) -> UserDM:
        user_dm = await self._user_reader.get_by_email(create_user_dto.email)

        if user_dm:
            if not user_dm.is_confirmed:
                await self._user_remover.remove_by_email(user_dm.email)

            else:
                raise FoundError('User already exists')

        hash_pwd = await self._pwd_hasher.hash(create_user_dto.password)

        user_dm = await self._user_saver.create(CreateUserDTO(
            email=create_user_dto.email,
            name=create_user_dto.name,
            password=hash_pwd,
            is_confirmed=False,
        ))

        registaration_code = await self._string_generator(EMAIL_CONFIRMATION_CODE_LENGTH)
        token_hash = await self._hasher.hash(registaration_code, self._security_config.hash_key)

        expires_at = datetime.now(tz=UTC) + timedelta(seconds=EMAIL_CONFIRMATION_TOKEN_TIME_SEC)

        await self._reg_token_saver.create(
            CreateRegisterTokenDTO(
                user_id=user_dm.id,
                token_hash=token_hash,
                type=RegistrationTokenType.EMAIL_CONFIRMATION,
                expires_at=expires_at,
            ),
        )

        await self._trx_manager.commit()

        return user_dm


class ConfirmUseUseCase:
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

    async def __call__(self, user_id: int, confirm_user_dto: ConfirmUserDTO) -> None:

        user_dm = await self._user_reader.get_by_id(user_id)

        if not user_dm:
            raise

        registration_token_dm = await self._reg_token_reader.get_by_user_id(user_dm.id)

        if not registration_token_dm:
            raise

        hash_code = await self._hasher.hash(confirm_user_dto.confirmation_code, self._config.security.hash_key)

        is_correct_code = await self._hasher.compare(hash_code, registration_token_dm.token_hash)

        if not is_correct_code:
            raise

        await self._user_editor.confirm_user_email(user_dm.id)
        await self._reg_token_editor.deactivate(registration_token_dm.id)

        await self._trx_manager.commit()
