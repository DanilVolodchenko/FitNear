from src.core.components.user.domain.entity import UserDM
from src.core.shared_kernel.application.interfaces.token import IAuthTokenReader
from src.core.shared_kernel.application.interfaces.security import IJWTToken
from src.core.shared_kernel.application.dto.security import JWTPayloadDTO
from config import SecurityConfig
from src.core.shared_kernel.application.exceptions.auth import AuthorizationError

class AuthorizationService:
    def __init__(
        self,
        security_config: SecurityConfig,
        jwt_token: IJWTToken,
        auth_token_reader: IAuthTokenReader,
    ) -> None:
        self._security_config = security_config
        self._jwt_token = jwt_token
        self._auth_token_reader = auth_token_reader

    async def get_user(self, access_token: str) -> UserDM:
        raw_payload = await self._jwt_token.decode(
            access_token, self._security_config.jwt_secret_key, self._security_config.jwt_algorithm
        )
        jwt_payload = JWTPayloadDTO(**raw_payload)

        auth_token = await self._auth_token_reader.get_by_id(jwt_payload.jti)

        if not auth_token or not auth_token.is_active:
            raise AuthorizationError('Invalid token')


