from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from controllers.http import router
from core.config import FastApiConfig
from di import ioc
from registrar.exception_handlers import register_fastapi_exception_handlers
from registrar.lifespan import lifespan


def register_fastapi_app(fastapi_config: FastApiConfig) -> FastAPI:
    app = FastAPI(**fastapi_config.model_dump(), lifespan=lifespan)

    setup_dishka(ioc, app)
    app.include_router(router)

    register_fastapi_exception_handlers(app)

    return app
