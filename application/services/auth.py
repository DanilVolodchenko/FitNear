from datetime import UTC, datetime, timedelta

from fastapi import Request, Response

from application.constants import EMAIL_CONFIRMATION_TOKEN_TIME_SEC, RANDOM_BYTES_COUNT
from application.domain.value_objects.token_type import RegistrationTokenType
from application.dto.security import JWTTokenDTO
from application.dto.token import CreateRegisterTokenDTO
from application.dto.user import CreateUserDTO, GetUserDTO
from application.errors import FoundError
from application.interfaces.localization import ITranslator
from application.interfaces.security import IHasher, IJWTToken, IPwdHasher, ITokenGenerator
from application.interfaces.token import (
    IRegistrationTokenReader,
    IRegistrationTokenSaver,
    IRegistrationTokenUpdater,
)
from application.interfaces.transaction import TransactionManager
from application.interfaces.user import IUserEmailConfirmer, IUserReader, IUserSaver
from core.config import Config
from infrastructure.utils.converter import get_language


class RegisterUserService:
    def __init__(
        self,
        config: Config,
        translator: ITranslator,
        user_reader: IUserReader,
        user_saver: IUserSaver,
        # user_email_confirmer: IUserEmailConfirmer,
        reg_token_reader: IRegistrationTokenReader,
        reg_token_saver: IRegistrationTokenSaver,
        reg_token_updater: IRegistrationTokenUpdater,
        pwd_hasher: IPwdHasher,
        token_generator: ITokenGenerator,
        hasher: IHasher,
        trx_manager: TransactionManager,
    ) -> None:
        self._config = config
        self._translator = translator
        self._user_reader = user_reader
        self._user_saver = user_saver
        # self._user_email_confirmer = user_email_confirmer
        self._reg_token_reader = reg_token_reader
        self._reg_token_saver = reg_token_saver
        self._reg_token_updater = reg_token_updater
        self._pwd_hasher = pwd_hasher
        self._token_generator = token_generator
        self._hasher = hasher
        self._trx_manager = trx_manager

    async def __call__(self, request: Request, user_dto: CreateUserDTO) -> None:

        user = await self._user_reader.get_by_email(user_dto.email)

        lang = get_language(request)

        if user:
            if not user.is_confirmed:
                await self._reg_token_updater.deactivate_by_user(user.id)

            else:
                raise FoundError(self._translator.translate('User already exists', lang=lang))

        hash_pwd = await self._pwd_hasher.hash(user_dto.password)
        user_dto.password = hash_pwd

        user_dm = await self._user_saver.create(user_dto)

        registaration_token = await self._token_generator(RANDOM_BYTES_COUNT)
        token_hash = await self._hasher.hash(registaration_token, self._config.security.hash_key)

        expires_at = datetime.now(tz=UTC) + timedelta(seconds=EMAIL_CONFIRMATION_TOKEN_TIME_SEC)

        registration_token_dm = await self._reg_token_saver.create(
            CreateRegisterTokenDTO(
                user_id=user_dm.id,
                token_hash=token_hash,
                type=RegistrationTokenType.EMAIL_CONFIRMATION,
                expires_at=expires_at,
            ),
        )

        await self._user_email_confirmer.send(
            self._config.server.confirmation_url,
            title='',
            description='',
        )


class LoginUserService:
    def __init__(
        self,
        config: Config,
        user_repository: IUserReader,
        jwt_token: IJWTToken,
        pwd_hasher: IPwdHasher,
        hasher: IHasher,
        translator: ITranslator,
    ) -> None:
        self._config = config
        self._user_repository = user_repository
        self._jwt_token = jwt_token
        self._pwd_hasher = pwd_hasher
        self._hasher = hasher
        self._translator = translator

    async def __call__(self, response: Response, user_dto: GetUserDTO) -> JWTTokenDTO:
        user = await self._user_repository.get_by_username(user_dto.username)
        if not user:
            raise ValueError(self._translator.translate('User Not Found', 'ru'))

        if not self._pwd_hasher.verify(user.password, user_dto.password):
            raise

        access_token = await self._jwt_token.encode(
            payload={'user_id': user.id, 'jti': 'uuid jwt токена'},
            secret_key=self._config.security.jwt_secret_key,
            algorithm=self._config.security.jwt_algorithm,
        )

        refresh_token = await self._jwt_token.encode(
            payload={'user_id': user.id, 'jti': 'uuid jwt токена'},
            secret_key=self._config.security.jwt_secret_key,
            algorithm=self._config.security.jwt_algorithm,
        )

        access_token = await self._hasher.hash(access_token, '1234')

        # response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)
        return JWTTokenDTO(access_token=access_token, refresh_token=refresh_token)


class LogoutUserService:
    def __init__(self) -> None:
        pass
