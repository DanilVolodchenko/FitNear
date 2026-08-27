from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.config import Config
from config.config_path import I18N_PATH
from di import ioc
from src.infrastructure.localization import ITranslator
from src.infrastructure.resources.database import create_db_if_not_exists


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    config = await ioc.get(Config)

    await create_db_if_not_exists(config.postgres)

    translator = await ioc.get(ITranslator)
    translator.compile(I18N_PATH)

    yield
