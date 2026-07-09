from enum import StrEnum
from typing import Any, Self

from dotenv import dotenv_values
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import URL

from core.config_path import ENV_PATH

env: dict[str, Any] = dotenv_values(ENV_PATH)


class ServerMode(StrEnum):
    DEV = 'DEV'
    TEST = 'TEST'
    PROD = 'PROD'


class FastApiConfig(BaseModel):
    title: str = Field('FitNear', alias='FASTAPI_TITLE')
    description: str = Field('CRM Service', alias='FASTAPI_DESCRIPTION')
    openapi_url: str | None = Field('/openapi.json', alias='FASTAPI_OPENAPI_URL')
    docs_url: str = Field('/api/docs', alias='FASTAPI_DOCS_URL')
    redoc_url: str = Field('/api/redoc', alias='FASTAPI_REDOC_URL')
    version: str = Field('0.0.0', alias='FASTAPI_VERSION')


class ServerConfig(BaseModel):
    mode: ServerMode = Field(ServerMode.PROD, alias='SERVER_MODE')
    dns: str = Field('localhost:8000', alias='SERVER_DNS')

    @property
    def http_url(self) -> str:
        protocol = 'http' if self.mode == ServerMode.DEV else 'https'
        return f'{protocol}://{self.dns}'

    @property
    def confirmation_url(self) -> str:
        return f'{self.http_url}/api/v1/user/confirm'


class PostgresConfig(BaseModel):
    host: str = Field('localhost', alias='POSTGRESQL_HOST')
    port: int = Field(5432, alias='POSTGRESQL_PORT')
    db: str = Field(alias='POSTGRESQL_DB')
    username: str = Field(alias='POSTGRESQL_USERNAME')
    pwd: str = Field(alias='POSTGRESQL_PWD')

    @property
    def uri(self) -> URL:
        return URL.create(
            drivername='postgresql+psycopg',
            host=self.host,
            port=self.port,
            database=self.db,
            username=self.username,
            password=self.pwd,
        )


class SecurityConfig(BaseModel):
    jwt_algorithm: str = Field('HS256', alias='SECURITY_JWT_ALGORITHM')
    jwt_secret_key: str = Field(alias='SECURITY_JWT_SECRET_KEY')
    hash_key: str = Field(alias='SECURITY_HASH_KEY')


class Config(BaseModel):
    fastapi: FastApiConfig = Field(default_factory=lambda: FastApiConfig(**env))
    server: ServerConfig = Field(default_factory=lambda: ServerConfig(**env))
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    security: SecurityConfig = Field(default_factory=lambda: SecurityConfig(**env))

    @model_validator(mode='after')
    def check_env(self) -> Self:
        if self.server.mode == ServerMode.PROD:
            self.fastapi.openapi_url = None

        return self


config: Config = Config()
