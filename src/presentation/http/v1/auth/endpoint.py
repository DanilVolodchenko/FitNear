from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, Security, status
from fastapi.security import HTTPAuthorizationCredentials

from src.core.components.user.application.constants import REFRESH_TOKEN_EXP_TIME_SEC
from src.core.components.user.application.dto import (
    ConfirmUserDTO,
    LoginUserDTO,
    LogoutUserDTO,
    RegisterSettingsDTO,
    RegisterUserDTO,
)
from src.core.components.user.application.service import (
    ConfirmUserService,
    LoginUserService,
    LogoutUserService,
    RegisterUserService,
)
from src.presentation.http.v1.auth.constant import COOKIE_REFRESH_TOKEN_NAME
from src.presentation.http.v1.auth.schemas.request import (
    ConfirmUserRequest,
    LoginUserRequest,
    RegisterUserRequest,
)
from src.presentation.http.v1.auth.schemas.response import LoginUserResponse, RegisteredUserResponse
from src.presentation.http.v1.deps import http_bearer

router = APIRouter(prefix='/auth', tags=['Auth'], route_class=DishkaRoute)


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    name='Регистрация пользователя',
)
async def register(
    user: RegisterUserRequest,
    register_user: FromDishka[RegisterUserService],
) -> RegisteredUserResponse:

    user_dto = RegisterUserDTO(
        email=user.email,
        name=user.name,
        password=user.password,
        settings=RegisterSettingsDTO(
            language=user.settings.language,
            theme=user.settings.theme,
        ),
    )
    registered_user_dto = await register_user(user_dto)

    return RegisteredUserResponse(
        registration_id=registered_user_dto.registration_id,
        expires_at=registered_user_dto.expires_at,
    )


@router.post(
    '/confirm/{registration_id}',
    status_code=status.HTTP_200_OK,
    name='Подтверждение почты пользователя.',
)
async def confirm(
    registration_id: UUID,
    user: ConfirmUserRequest,
    confirm_user: FromDishka[ConfirmUserService],
) -> None:

    confirm_user_dto = ConfirmUserDTO(confirmation_code=user.confirmation_code)

    return await confirm_user(registration_id, confirm_user_dto)


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    name='Авторизация пользователя',
)
async def login(
    request: Request,
    response: Response,
    login_user_schema: LoginUserRequest,
    login_user: FromDishka[LoginUserService],
) -> LoginUserResponse:

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get('user-agent')

    login_user_dto = LoginUserDTO(
        email=login_user_schema.email,
        password=login_user_schema.password,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    jwt_token_dto = await login_user(login_user_dto)

    response.set_cookie(
        COOKIE_REFRESH_TOKEN_NAME,
        jwt_token_dto.refresh_token,
        httponly=True,
        secure=True,
        samesite='strict',
        max_age=REFRESH_TOKEN_EXP_TIME_SEC,
    )

    return LoginUserResponse(access_token=jwt_token_dto.access_token)


@router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
    name='Деавторизация пользователя',
)
async def logout(
    request: Request,
    response: Response,
    bearer_schema: Annotated[HTTPAuthorizationCredentials, Security(http_bearer)],
    logout_user: FromDishka[LogoutUserService],
) -> None:
    access_token = bearer_schema.credentials if bearer_schema else None
    refresh_token = request.cookies.get(COOKIE_REFRESH_TOKEN_NAME)

    logout_user_dto = LogoutUserDTO(access_token=access_token, refresh_token=refresh_token)

    await logout_user(logout_user_dto)

    response.delete_cookie(
        COOKIE_REFRESH_TOKEN_NAME,
        httponly=True,
        secure=True,
        samesite='strict',
    )
