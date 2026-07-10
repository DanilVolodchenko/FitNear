from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, status

from application.dto.user import CreateUserDTO, GetUserDTO
from application.interfaces.transaction import ITransactionManager
from application.services.auth import RegisterUserService
from controllers.schemas.user import LoginUserSchema, RegisterUserSchema

router = APIRouter(prefix='/auth', tags=['Auth'], route_class=DishkaRoute)


@router.post('/register', status_code=status.HTTP_201_CREATED, name='Регистрация пользователя')
async def register(
    request: Request,
    user: RegisterUserSchema,
    register_user: FromDishka[RegisterUserService],
    trx_manager: FromDishka[ITransactionManager],
):

    user_dto = CreateUserDTO(
        email=user.email,
        name=user.name,
        password=user.password,
    )
    res = await register_user(request, user_dto)
    await trx_manager.commit()

    return res
