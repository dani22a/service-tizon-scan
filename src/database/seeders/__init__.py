from src.database.seeders.user_seeder import seed_users
from src.database.seeders.cultivo_seeder import seed_cultivo
from src.database.seeders.periodo_seeder import seed_periodos
from src.database.start.connection import start_connection
from src.database.start.connection import stop_connection

async def seed_database():
  
  # Iniciamos con la conexion a la base de datos
  await start_connection()
  
  # Ejecutamos los seeders
  await seed_users()
  await seed_cultivo()
  await seed_periodos()
  
  # Cerramos la conexion a la base de datos
  await stop_connection()