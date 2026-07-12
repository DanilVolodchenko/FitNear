import asyncio
import secrets

from application.interfaces.generator import IRandomGenerator


class RandomStringGenerator(IRandomGenerator):
    async def __call__(self, count: int) -> str:
        return await asyncio.to_thread(secrets.token_urlsafe, count)


class RandomNumberGenerator(IRandomGenerator):
