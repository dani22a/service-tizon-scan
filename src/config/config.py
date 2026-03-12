from pydantic_settings import BaseSettings
from typing import Literal

class Config(BaseSettings):
  PORT: int
  DEBUG: bool
  DOMAIN: str
  ENV: Literal["development", "production"]
  NAME_COOKIE: str
  ROBOFLOW_API_URL: str = "https://serverless.roboflow.com"
  ROBOFLOW_API_KEY: str | None = None
  ROBOFLOW_MODEL_ID: str | None = None
  ROBOFLOW_TIMEOUT_SEC: int = 15
  MAX_IMAGE_SIZE_MB: int = 10
  
  class Config: 
      env_file = ".env"
      extra = "ignore"
