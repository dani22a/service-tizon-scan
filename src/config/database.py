from pydantic_settings import BaseSettings

class DatabaseConfig(BaseSettings):
  
  DB_HOST: str
  DB_PORT: int
  DB_USER: str
  DB_PASSWORD: str
  DB_NAME: str
  
  class Config: 
      env_file = ".env"
      extra = "ignore"
