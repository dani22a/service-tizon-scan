from .config import Config
from functools import lru_cache
from .database import DatabaseConfig
from .jwt import JWTConfig

@lru_cache()
def get_config():
    return Config()

@lru_cache()
def get_database_config():
    return DatabaseConfig()

@lru_cache()
def get_jwt_config():
    return JWTConfig()