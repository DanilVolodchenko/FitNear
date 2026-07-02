from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import Request


def get_language(request: 'Request') -> str:
    primary_lang = request.headers.get('accept-language', 'ru')
    lang = primary_lang.split(',')[0]

    return lang.split('-')[0]
