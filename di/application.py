from dishka import Provider, Scope, provide

from application.services.auth import RegisterUserService, LoginUserService


class ApplicationProvider(Provider):
    register_user_service = provide(
        RegisterUserService, scope=Scope.REQUEST
    )

    login_user_service = provide(
        LoginUserService, scope=Scope.REQUEST
    )
