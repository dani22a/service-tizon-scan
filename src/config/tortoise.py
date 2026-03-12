from src.config.database import DatabaseConfig
from tortoise.config import TortoiseConfig, DBUrlConfig, AppConfig

database_config = DatabaseConfig()

db_host = "127.0.0.1" if database_config.DB_HOST in ("localhost", "::1") else database_config.DB_HOST

db_url = f"postgres://{database_config.DB_USER}:{database_config.DB_PASSWORD}@{db_host}:{database_config.DB_PORT}/{database_config.DB_NAME}"

tortoise_config = TortoiseConfig(
  connections={
    "default": DBUrlConfig(url=db_url),
  },
  apps={
    "models": AppConfig(
      models=["src.models"],
      default_connection="default",
    ),
  },
  use_tz=True,
  timezone="UTC"
)