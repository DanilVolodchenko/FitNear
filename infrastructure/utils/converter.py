from fastapi import Request


def get_language(request: Request) -> str:
    primary_lang = request.headers.get('accept-language', 'ru_RU')
    lang = primary_lang.split(',')[0]

    return lang.replace('-', '_')
