"""Config."""

from pydantic import EmailStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralSettings(BaseSettings):
    """General settings."""

    cors_origins: list[str]
    api_prefix: str = "/api"


class DatabaseSettings(BaseSettings):
    """Database settings."""

    url: PostgresDsn


class JWTSettings(BaseSettings):
    """JWT settings."""

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours


class EmailSettings(BaseSettings):
    """Email settings."""

    mail_from: EmailStr


class SMTPBZSettings(BaseSettings):
    """SMTP.BZ settings."""

    api_url: str
    api_key: str


class S3Settings(BaseSettings):
    """S3 settings."""

    access_key_id: str
    secret_access_key: str
    region_name: str = "ru-central1"
    bucket_name: str
    endpoint_url: str


class Settings(BaseSettings):
    """Settings config."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__", extra="ignore"
    )

    general: GeneralSettings
    database: DatabaseSettings
    jwt: JWTSettings
    s3: S3Settings


settings = Settings()
