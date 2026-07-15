from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from di import ioc
from src.core.errors import ApplicationError
from src.core.interfaces.localization import ITranslator
from src.core.interfaces.log import ILogger


def register_fastapi_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationError)
    async def application_error_handler(request: Request, exc: ApplicationError) -> JSONResponse:
        logger = await ioc.get(ILogger)

        logger.error('Application Error: ({}) {}', exc.__class__.__name__, exc)

        return JSONResponse(
            content={'detail': f'{exc}'},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
        translator = await ioc.get(ITranslator)
        logger = await ioc.get(ILogger)

        lang_code = translator.get_lang_code(request)

        logger.error('Unexpected error: ({}) {}', exc.__class__.__name__, exc)

        return JSONResponse(
            content={'detail': translator.translate('Internal Server Error', lang_code=lang_code)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
