from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.controller.http.v1.schemas.user import ConfirmUserSchema, RegisterUserSchema
from src.core.components.user.application.dto import ConfirmUserDTO, CreateUserDTO
from src.core.components.user.application.use_case import ConfirmUseUseCase, RegisterUserUseCase

router = APIRouter(prefix='/auth', tags=['Auth'], route_class=DishkaRoute)


@router.post('/register', status_code=status.HTTP_201_CREATED, name='Регистрация пользователя')
async def register(
    user: RegisterUserSchema,
    register_user: FromDishka[RegisterUserUseCase],
) -> None:

    user_dto = CreateUserDTO(
        email=user.email,
        name=user.name,
        password=user.password,
    )
    return await register_user(user_dto)


@router.post('/confirm/{user_id}', status_code=status.HTTP_204_NO_CONTENT, name='Подтверждение почты пользователя.')
async def confirm(
    user_id: int,
    user: ConfirmUserSchema,
    confirm_user: FromDishka[ConfirmUseUseCase],
) -> None:

    confirm_user_dto = ConfirmUserDTO(
        confirmation_code=user.confirmation_code,
    )

    return await confirm_user(user_id, confirm_user_dto)
