from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, status

from src.controllers.schemas.user import RegisterUserSchema
from src.core.dto.user import CreateUserDTO
from src.core.services.auth import RegisterUserService

router = APIRouter(prefix='/auth', tags=['Auth'], route_class=DishkaRoute)


@router.post('/register', status_code=status.HTTP_201_CREATED, name='Регистрация пользователя')
async def register(
    request: Request,
    user: RegisterUserSchema,
    register_user: FromDishka[RegisterUserService],
) -> None:

    user_dto = CreateUserDTO(
        email=user.email,
        name=user.name,
        password=user.password,
    )
    return await register_user(request, user_dto)


@router.post('/confirm', status_code=status.HTTP_201_CREATED, name='Подтверждение почты пользователя.')
async def confirm() -> None:
    pass
