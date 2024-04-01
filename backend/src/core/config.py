
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    PostgresDsn,
    computed_field,
)
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''
    POSTGRES_DB: str = ""
    SMTP_PORT: int = 465
    SMTP_HOST: str = ''
    SMTP_USER: str = ''
    SMTP_PASSWORD: str = ''
    EMAILS_FROM_EMAIL: str = ''
    SECRET_KEY: str = ''
    CLOUDINARY_CLOUD_NAME: str = ''
    CLOUDINARY_API_KEY: str = ''
    CLOUDINARY_API_SECRET: str = ''
    ALGORITHM: str = 'HS256'
    FRONTEND_URL: str = 'http://localhost:3000'
    BACKEND_URL: str = 'http://localhost:8000'
    ADMINER_URL: str = 'http://localhost:8080/?pgsql=localhost&username=&db=&ns=&passwd='
    REDIS_HOST_: str = 'redis'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ''

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()
