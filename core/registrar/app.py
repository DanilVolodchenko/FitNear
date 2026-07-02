from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from controllers.http import router
from core.config import FastApiConfig
from core.registrar.exception_handlers import register_exception_handlers
from core.registrar.lifespan import lifespan
from di import ioc


def register_app(fastapi_config: FastApiConfig) -> FastAPI:
    app = FastAPI(**fastapi_config.model_dump(), lifespan=lifespan)

    setup_dishka(ioc, app)
    app.include_router(router)

    register_exception_handlers(app)

    return app
