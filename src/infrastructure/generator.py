import asyncio
import secrets
import string
from uuid import UUID, uuid4

from src.core.shared_kernel.application.interfaces.generator import IStringGenerator, IUUIDGenerator


class StringDigitCodeGenerator(IStringGenerator):
    async def __call__(self, length: int) -> str:
        return ''.join([secrets.choice(string.digits) for _ in range(length)])


class UUID4Generator(IUUIDGenerator):
    async def __call__(self) -> UUID:
        return await asyncio.to_thread(uuid4)