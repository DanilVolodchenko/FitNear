from dishka.integrations.taskiq import setup_dishka

from di import ioc
from src.infrastructure.resources.broker import redis_list_queue_broker

setup_dishka(ioc, redis_list_queue_broker)
