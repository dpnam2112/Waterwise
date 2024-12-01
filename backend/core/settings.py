import os
from typing import Literal

from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class CoreSettings(BaseSettings):
    ENV: Literal["development", "production"] = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARN", "ERROR", "FATAL"] = "DEBUG"


class TestSettings(BaseSettings):
    PYTEST: bool = False
    PYTEST_UNIT: bool = False


class DatabaseSettings(BaseSettings):
    SQLALCHEMY_POSTGRES_URI: str = "postgresql+asyncpg://postgres:thangcho@127.0.0.1:5432/fastapi_seed"
    SQLALCHEMY_ECHO: bool = False


class RedisSettings(BaseSettings):
    REDIS_URL: str = "redis://127.0.0.1:6379/0"

class GoogleSettings(BaseSettings):
    model_config =  SettingsConfigDict(extra='ignore')

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_CALLBACK_URI: str = "http://localhost:8080/v1/auth/google/callback"

    GOOGLE_API_BASE_URI: str = "https://www.googleapis.com"
    GOOGLE_PEOPLE_API_BASE_URI: str = "https://www.people.googleapis.com"
    GOOGLE_AUTH_URL: str = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL: str = "https://oauth2.googleapis.com/token"
    GOOGLE_SCOPES: list[str] = ["openid", "email", "profile"]

class Settings(
    CoreSettings,
    TestSettings,
    DatabaseSettings,
    RedisSettings,
    GoogleSettings
): ...


class DevelopmentSettings(Settings): ...

class ProductionSettings(Settings):
    DEBUG: bool = False


def get_settings() -> Settings:
    kwargs = {"_env_file": ".env"}
    env = os.getenv("ENV", "development")
    setting_types = {
        "development": DevelopmentSettings(**kwargs),
        "production": ProductionSettings(**kwargs),
    }
    return setting_types[env]


settings = get_settings()
