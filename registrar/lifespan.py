from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.localization import compile_translations


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    compile_translations()

    yield
