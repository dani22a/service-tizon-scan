from pydantic_settings import BaseSettings

class JWTConfig(BaseSettings):
  JWT_SECRET: str
  JWT_EXPIRATION: int
  
  class Config: 
      env_file = ".env"
      extra = "ignore"
