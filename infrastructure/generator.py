import secrets
import string

from application.interfaces.generator import IStringGenerator


class StringDigitCodeGenerator(IStringGenerator):
    async def __call__(self, length: int) -> str:
        return ''.join([secrets.choice(string.digits) for _ in range(length)])
