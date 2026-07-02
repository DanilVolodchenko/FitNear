from fastapi import Request, Response

from application.dto.security import JWTTokenDTO
from application.dto.user import CreateUserDTO, GetUserDTO
from application.errors import FoundError
from application.interfaces.localization import ITranslator
from application.interfaces.security import IHasher, IJWTToken, IPwdHasher
from application.interfaces.transaction import TransactionManager
from application.interfaces.user import IUserReader, IUserSaver
from core.config import Config
from infrastructure.utils.converter import get_language


class RegisterUserService:
    def __init__(
        self,
        user_reader: IUserReader,
        trx_manager: TransactionManager,
        user_saver: IUserSaver,
        pwd_hasher: IPwdHasher,
        translator: ITranslator,
    ) -> None:
        self._user_reader = user_reader
        self._user_saver = user_saver
        self._pwd_hasher = pwd_hasher
        self._trx_manager = trx_manager
        self._translator = translator

    async def __call__(self, request: Request, user_dto: CreateUserDTO) -> None:

        user = await self._user_reader.get_by_email(user_dto.email)

        lang = get_language(request)

        if user:
            raise FoundError(self._translator.translate('User already exists', lang=lang))

        user_dto.password = await self._pwd_hasher.hash(user_dto.password)

        await self._user_saver.create(user_dto)


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
