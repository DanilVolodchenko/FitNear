from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.config_path import I18N_PATH
from di import ioc
from src.infrastructure.localization import ITranslator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    translator = await ioc.get(ITranslator)
    translator.compile(I18N_PATH)

    yield
