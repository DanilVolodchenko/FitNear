from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from di import ioc
from infrastructure.localization import Translator, ITranslator
from infrastructure.utils.converter import get_language


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(Exception)
    async def unexpected_exc_handler(request: Request, exc: Exception) -> JSONResponse:
        translator = await ioc.get(ITranslator)
        lang = get_language(request)

        logger.error('Unexpected error: ({}) {}', exc.__class__.__name__, exc)

        return JSONResponse(
            content={'detail': translator.translate('Internal Server Error', lang=lang)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
