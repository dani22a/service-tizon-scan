from tortoise import Tortoise
import logging
from src.config.tortoise import tortoise_config

logger = logging.getLogger("LOGGER_DATABASE")

async def start_connection():
  await Tortoise.init(config=tortoise_config, _enable_global_fallback=True)
  logger.info("Conexion a la base de datos establecida correctamente")
  
  await Tortoise.generate_schemas()
  logger.info("Esquemas de la base de datos generados correctamente")

async def stop_connection():
  await Tortoise.close_connections()
  logger.info("Conexion a la base de datos cerrada correctamente")