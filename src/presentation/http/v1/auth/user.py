from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, status

from src.core.components.user.application.constants import REFRESH_TOKEN_EXP_TIME_SEC
from src.core.components.user.application.dto import (
    ConfirmUserDTO,
    LoginUserDTO,
    RegisterSettingsDTO,
    RegisterUserDTO,
)
from src.core.components.user.application.service import (
    ConfirmUserService,
    LoginUserService,
    LogoutUserService,
    RegisterUserService,
)
from src.presentation.http.v1.auth.schemas.request import ConfirmUserRequest, LoginUserRequest, RegisterUserRequest
from src.presentation.http.v1.auth.schemas.response import LoginUserResponse, RegisteredUserResponse

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
    status_code=status.HTTP_204_NO_CONTENT,
    name='Подтверждение почты пользователя.',
)
async def confirm(
    registration_id: int,
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
    user: LoginUserRequest,
    login_user: FromDishka[LoginUserService],
) -> LoginUserResponse:

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get('user-agent')

    login_user_dto = LoginUserDTO(
        email=user.email,
        password=user.password,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    jwt_token_dto = await login_user(login_user_dto)

    response.set_cookie(
        'refresh_token',
        jwt_token_dto.refresh,
        httponly=True,
        secure=True,
        samesite='strict',
        max_age=REFRESH_TOKEN_EXP_TIME_SEC,
    )

    return LoginUserResponse(access=jwt_token_dto.access)


@router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
    name='Деавторизация пользователя',
)
async def logout(
    logout_user: FromDishka[LogoutUserService],
):
    await logout_user()
