from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from config import FastApiConfig
from di import ioc
from registrar.error_handlers import register_fastapi_error_handlers
from registrar.lifespan import lifespan
from src.controllers.http import router


def register_fastapi_app(fastapi_config: FastApiConfig) -> FastAPI:
    app = FastAPI(**fastapi_config.model_dump(), lifespan=lifespan)

    setup_dishka(ioc, app)
    app.include_router(router)

    register_fastapi_error_handlers(app)

    return app
