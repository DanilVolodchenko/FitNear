from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any


class IJWTToken(ABC):
    @abstractmethod
    async def encode(self, payload: dict[str, Any], *, secret_key: str, algorithm: str) -> str:
        """Encode payload to jwt token."""

    @abstractmethod
    async def decode(self, token: str, secret_key: str, algorithms: Sequence[str]) -> dict[str, Any]:
        """Decode from jwt token to payload."""


class IHasher(ABC):
    @abstractmethod
    async def hash(self, msg: str, key: str) -> str:
        """Hash msg using key."""

    @abstractmethod
    async def compare(self, hash_msg_1: str | bytes, hash_msg_2: str | bytes) -> bool:
        """Compare hash_msg_1 and hash_msg_2."""


class IPwdHasher(ABC):
    @abstractmethod
    async def hash(self, password: str | bytes, salt: bytes | None = None) -> str:
        """Hash password. Returns hash string."""

    @abstractmethod
    async def verify(self, hash_password: str, password: str) -> bool:
        """Verify hash_password and password."""

    @abstractmethod
    async def check_needs_rehash(self, pwd_hash: str) -> bool:
        """Check need to rehash hash or not."""
