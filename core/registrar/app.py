from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from controllers.http import router
from core.config import FastApiConfig
from di import ioc


def register_app(fastapi_config: FastApiConfig) -> FastAPI:
    app = FastAPI(**fastapi_config.model_dump())

    setup_dishka(ioc, app)
    app.include_router(router)

    return app
