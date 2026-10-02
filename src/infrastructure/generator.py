import secrets
import string
from uuid import UUID, uuid4, uuid7

from src.core.shared_kernel.application.interfaces.generator import IStringGenerator, IUUIDGenerator


class StringDigitCodeGenerator(IStringGenerator):
    def generate(self, length: int) -> str:
        return ''.join([secrets.choice(string.digits) for _ in range(length)])


class UUID4Generator(IUUIDGenerator):
    def generate(self) -> UUID:
        return uuid4()


class UUID7Generator(IUUIDGenerator):
    def generate(self) -> UUID:
        return uuid7()
