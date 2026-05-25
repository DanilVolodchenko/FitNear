from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Response, status

from application.services.auth import RegisterUserService, LoginUserService
from controllers.schemas.user import LoginUserSchema, RegisterUserSchema
from application.dto.user import GetUserDTO, CreateUserDTO

router = APIRouter(prefix='/auth', tags=['Auth'], route_class=DishkaRoute)


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
)
async def register(
        user: RegisterUserSchema,
        register_user: FromDishka[RegisterUserService]
) -> None:
    user_dto = CreateUserDTO(
        username=user.username,
        name=user.name,
        password=user.password,
    )
    await register_user(user_dto)


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
)
async def login(
        response: Response,
        user: LoginUserSchema,
        login_user: FromDishka[LoginUserService]
):
    user = GetUserDTO(
        username=user.username,
        password=user.password
    )
    return await login_user(response, user)


@router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
)
async def logout():
    ...
