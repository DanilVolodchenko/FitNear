from typing import Literal

from dotenv import dotenv_values
from pydantic import BaseModel, Field
from sqlalchemy import URL
from os import environ
from core.config_path import ENV_PATH

env = dotenv_values(ENV_PATH)

print(environ)


class FastApiConfig(BaseModel):
    title: str = Field('FitNear', alias='FASTAPI_TITLE')
    description: str = Field('CRM Service', alias='FASTAPI_DESCRIPTION')
    doc_url: str = Field('/api/docs', alias='FASTAPI_DOC_URL')
    redoc_url: str = Field('/api/redoc', alias='FASTAPI_REDOC_URL')
    version: str = Field('0.0.0', alias='FASTAPI_VERSION')


class ServerConfig(BaseModel):
    mode: Literal['prod', 'dev', 'test'] = Field('prod', alias='SERVER_MODE')


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
    jwt_algorithm: str = Field('HS512', alias='SECURITY_JWT_ALGORITHM')
    jwt_secret_key: str = Field(alias='SECURITY_JWT_SECRET_KEY')


class Config(BaseModel):
    fastapi: FastApiConfig = Field(default_factory=lambda: FastApiConfig(**env))
    server: ServerConfig = Field(default_factory=lambda: ServerConfig(**env))
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    security: SecurityConfig = Field(default_factory=lambda: SecurityConfig(**env))


config: Config = Config()
