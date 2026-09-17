from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.controller.http.v1.schemas.user import ConfirmUserSchema, LoginUserSchema, RegisterUserSchema
from src.core.components.user.application.dto import (
    ConfirmUserDTO,
    LoginUserDTO,
    RegisteredUserDTO,
    RegisterSettingsDTO,
    RegisterUserDTO,
)
from src.core.components.user.application.service import (
    ConfirmUserService,
    LoginUserService,
    LogoutUserService,
    RegisterUserService,
)

router = APIRouter(prefix='/auth', tags=['Auth'], route_class=DishkaRoute)


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    name='Регистрация пользователя',
)
async def register(
    user: RegisterUserSchema,
    register_user: FromDishka[RegisterUserService],
) -> RegisteredUserDTO:

    user_dto = RegisterUserDTO(
        email=user.email,
        name=user.name,
        password=user.password,
        settings=RegisterSettingsDTO(
            language=user.settings.language,
            theme=user.settings.theme,
        ),
    )
    return await register_user(user_dto)


@router.post(
    '/confirm/{registration_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    name='Подтверждение почты пользователя.',
)
async def confirm(
    registration_id: int,
    user: ConfirmUserSchema,
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
    user: LoginUserSchema,
    login_user: FromDishka[LoginUserService],
):
    login_user_dto = LoginUserDTO(email=user.email, password=user.password)
    return await login_user(login_user_dto)


@router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
    name='Деавторизация пользователя',
)
async def logout(
    logout_user: FromDishka[LogoutUserService],
):
    await logout_user()
