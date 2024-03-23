
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    PostgresDsn,
    computed_field,
)
from pydantic_core import MultiHostUrl
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""
    SMTP_PORT: int = 465
    SMTP_HOST: str = ''
    SMTP_USER: str = ''
    SMTP_PASSWORD: str = ''
    EMAILS_FROM_EMAIL: str = ''
    SECRET_KEY: str = 'secret_key'
    ALGORITHM: str = 'HS256'
    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()