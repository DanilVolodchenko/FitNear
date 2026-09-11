from dishka.integrations.fastapi import setup_dishka

from config import config
from di import ioc
from registrar import register_fastapi_app

app = register_fastapi_app(config.fastapi)

setup_dishka(ioc, app)
