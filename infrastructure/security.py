import asyncio
import hmac
from collections.abc import Sequence
from hashlib import sha256
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error, InvalidHashError

from application.interfaces.security import IHasher, IJWTToken, IPwdHasher


class JWTToken(IJWTToken):
    async def encode(self, payload: dict[str, Any], secret_key: str, algorithm: str) -> str:
        return await asyncio.to_thread(jwt.encode, payload=payload, key=secret_key, algorithm=algorithm)

    async def decode(self, token: str, secret_key: str, algorithms: Sequence[str]) -> dict[str, Any]:
        return await asyncio.to_thread(jwt.decode, jwt=token, key=secret_key, algorithms=algorithms)


class Argon2PwdHasher(IPwdHasher):
    def __init__(self) -> None:
        self.ph = PasswordHasher()

    async def hash(self, password: str | bytes, salt: bytes | None = None) -> str:
        return await asyncio.to_thread(self.ph.hash, password=password, salt=salt)

    async def verify(self, hash_password: str, password: str) -> bool:
        try:
            await asyncio.to_thread(self.ph.verify, hash=password, password=password)
        except InvalidHashError, Argon2Error:
            return False
        return True

    async def check_needs_rehash(self, pwd_hash: str) -> bool:
        return await asyncio.to_thread(self.ph.check_needs_rehash, hash=pwd_hash)


class SHA256Hasher(IHasher):
    async def hash(self, msg: str, key: str) -> str:
        return hmac.new(
            key=key.encode(encoding='utf-8'),
            msg=msg.encode(encoding='utf-8'),
            digestmod=sha256,
        ).hexdigest()

    async def compare(self, hash_msg_1: str | bytes, hash_msg_2: str | bytes) -> bool:
        return hmac.compare_digest(hash_msg_1, hash_msg_2)
