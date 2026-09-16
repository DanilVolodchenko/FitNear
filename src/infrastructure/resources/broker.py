from collections.abc import AsyncGenerator
from typing import Final

from redis import exceptions
from redis.asyncio import Redis
from taskiq_redis.redis_broker import ListQueueBroker

from config import config

BROKER_DB: Final[int] = 0
QUEUE_NAME: Final[str] = 'bg_tasks'


class RedisListQueueBroker(ListQueueBroker):
    async def listen(self) -> AsyncGenerator[bytes]:
        """
        Метод переопределен, чтобы обработать ошибку TimeoutError, иначе воркер падает с ошибкой.
        Issue: https://github.com/taskiq-python/taskiq-redis/issues/127
        """

        redis_brpop_data_position = 1
        while True:
            try:
                async with Redis(connection_pool=self.connection_pool) as redis_conn:
                    brpop_result = await redis_conn.brpop(self.queue_name)
                    if brpop_result is None:
                        continue
                    yield brpop_result[redis_brpop_data_position]
            except ConnectionError:
                continue
            except exceptions.TimeoutError:
                continue


redis_list_queue_broker = RedisListQueueBroker(f'{config.redis.dsn}/{BROKER_DB}', queue_name=QUEUE_NAME)
