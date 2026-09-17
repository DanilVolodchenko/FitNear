from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from di import ioc
from src.core.exceptions.app_logic import AppError
from src.core.shared_kernel.application.interfaces.localization import ITranslator
from src.core.shared_kernel.application.interfaces.log import ILogger


def register_fastapi_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppError)
    async def application_error_handler(request: Request, exc: AppError) -> JSONResponse:
        translator = await ioc.get(ITranslator)
        logger = await ioc.get(ILogger)

        lang_code = translator.get_lang_code(request)

        logger.error('Application Error: ({}) {}', exc.__class__.__name__, exc)

        return JSONResponse(
            content={'detail': f'{translator.translate(str(exc), lang_code=lang_code)}'},
            status_code=HTTPStatus.BAD_REQUEST,
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
