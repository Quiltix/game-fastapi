"""Config."""

from pydantic import EmailStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralSettings(BaseSettings):
    """Основные настройки."""

    cors_origins: list[str]
    api_prefix: str = "/api"


class DatabaseSettings(BaseSettings):
    """Настройки БД."""

    url: PostgresDsn


class JWTSettings(BaseSettings):
    """Настройки JWT."""

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

class Settings(BaseSettings):
    """Класс настроек."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__", extra="ignore"
    )

    general: GeneralSettings
    database: DatabaseSettings
    jwt: JWTSettings


settings = Settings()
