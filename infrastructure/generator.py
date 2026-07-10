import asyncio
import secrets

from application.interfaces.generator import IStringGenerator


class RandomStringGenerator(IStringGenerator):
    async def __call__(self, bytes_count: int) -> str:
        return await asyncio.to_thread(secrets.token_urlsafe, bytes_count)
