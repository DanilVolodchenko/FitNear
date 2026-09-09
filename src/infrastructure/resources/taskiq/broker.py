from collections.abc import AsyncGenerator

from redis import exceptions
from redis.asyncio import Redis
from taskiq_redis.redis_broker import ListQueueBroker


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
                    yield brpop_result[redis_brpop_data_position]  # type: ignore[misc]
            except ConnectionError:
                continue
            except exceptions.TimeoutError:
                continue


redis_broker = RedisListQueueBroker('redis://localhost:6379/8')
