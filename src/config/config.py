from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PORT: int = 80
    DEBUG: bool = False
    DOMAIN: str = ""
    ENV: Literal["development", "production"] = "production"

    GENERATE_SCHEMAS: bool = False

    NAME_COOKIE: str = "access_token"

    CORS_ORIGINS: str = "http://localhost:3000"

    ROBOFLOW_API_URL: str = "https://serverless.roboflow.com"
    ROBOFLOW_API_KEY: str | None = None
    ROBOFLOW_MODEL_ID: str | None = None
    ROBOFLOW_TIMEOUT_SEC: int = 15
    MAX_IMAGE_SIZE_MB: int = 10