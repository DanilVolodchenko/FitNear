import uvicorn
from dishka.integrations.fastapi import setup_dishka as fastapi_setup_dishka
from dishka.integrations.taskiq import setup_dishka as taskiq_setup_dishka

from config import config
from di import ioc
from registrar import register_fastapi_app
from src.infrastructure.resources.taskiq import redis_broker

app = register_fastapi_app(config.fastapi)

fastapi_setup_dishka(ioc, app)
taskiq_setup_dishka(ioc, redis_broker)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
