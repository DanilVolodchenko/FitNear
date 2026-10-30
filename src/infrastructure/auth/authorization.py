from datetime import UTC, datetime

import jwt

from config import SecurityConfig
from src.core.components.user.application.interface import IUserReader
from src.core.components.user.domain.entity import UserDM
from src.core.shared_kernel.application.dto.security import JWTPayloadDTO
from src.core.shared_kernel.application.exceptions.auth import AuthorizationError
from src.core.shared_kernel.application.interfaces.security import IJWTToken


class AuthorizationService:
    def __init__(
        self,
        security_config: SecurityConfig,
        jwt_token: IJWTToken,
        user_reader: IUserReader,
    ) -> None:
        self._security_config = security_config
        self._jwt_token = jwt_token
        self._user_reader = user_reader

    async def get_user(self, access_token: str) -> UserDM:
        jwt_payload = await self.validate_jwt_token(access_token)

        user = await self._user_reader.get_by_id(jwt_payload.sub)

        if not user:
            raise AuthorizationError('User not found')

        return user

    async def validate_jwt_token(self, jwt_token: str) -> JWTPayloadDTO:
        try:
            raw_payload = await self._jwt_token.decode(
                jwt_token,
                self._security_config.jwt_secret_key,
                self._security_config.jwt_decode_algorithms,
            )
        except jwt.PyJWTError:
            raise AuthorizationError('Invalid token')

        jwt_payload = JWTPayloadDTO.from_dict(raw_payload)

        if jwt_payload.exp < datetime.now(tz=UTC):
            raise AuthorizationError('Token was expired')

        return jwt_payload
