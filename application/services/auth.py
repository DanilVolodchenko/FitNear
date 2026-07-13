from datetime import UTC, datetime, timedelta

from fastapi import Request

from application.constants import EMAIL_CONFIRMATION_CODE_LENGTH, EMAIL_CONFIRMATION_TOKEN_TIME_SEC
from application.domain.value_objects.token_type import RegistrationTokenType
from application.dto.token import CreateRegisterTokenDTO
from application.dto.user import CreateUserDTO
from application.errors import FoundError
from application.interfaces.generator import IStringGenerator
from application.interfaces.localization import ITranslator
from application.interfaces.repositories import (
    IRegistrationTokenSaver,
    IUserReader,
    IUserRemover,
    IUserSaver,
)
from application.interfaces.security import IHasher, IPwdHasher
from application.interfaces.transaction import ITransactionManager
from core.config import Config


class RegisterUserService:
    def __init__(
        self,
        config: Config,
        translator: ITranslator,
        user_reader: IUserReader,
        user_saver: IUserSaver,
        user_remover: IUserRemover,
        reg_token_saver: IRegistrationTokenSaver,
        pwd_hasher: IPwdHasher,
        string_generator: IStringGenerator,
        hasher: IHasher,
        trx_manager: ITransactionManager,
    ) -> None:
        self._config = config
        self._translator = translator
        self._user_reader = user_reader
        self._user_saver = user_saver
        self._user_remover = user_remover
        self._reg_token_saver = reg_token_saver
        self._pwd_hasher = pwd_hasher
        self._string_generator = string_generator
        self._hasher = hasher
        self._trx_manager = trx_manager

    async def __call__(self, request: Request, user_dto: CreateUserDTO) -> None:
        user = await self._user_reader.get_by_email(user_dto.email)

        lang_code = self._translator.get_lang_code(request)

        if user:
            if not user.is_confirmed:
                await self._user_remover.remove_by_email(user.email)

            else:
                raise FoundError(self._translator.translate('User already exists', lang_code))

        hash_pwd = await self._pwd_hasher.hash(user_dto.password)
        user_dto.password = hash_pwd

        user_dm = await self._user_saver.create(user_dto)

        registaration_token = await self._string_generator(EMAIL_CONFIRMATION_CODE_LENGTH)
        token_hash = await self._hasher.hash(registaration_token, self._config.security.hash_key)

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
