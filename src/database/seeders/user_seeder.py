from src.models import User
from src.lib.bycript import hash_password
import logging

logger = logging.getLogger("LOGGER SEED")

async def seed_users():
  users_data = [
    {
      "username": "JoseGuti",
      "password": hash_password("123456"),
      "email": "joseluisjlgd123@gmail.com",
      "full_name": "Jose Gutierrez",
    }
  ]
  
  for user_data in users_data:
    # Usar get_or_create para evitar duplicados
    user, created = await User.get_or_create(
      email=user_data["email"],
      defaults={
        "username": user_data["username"],
        "password": user_data["password"],
        "full_name": user_data["full_name"],
      }
    )
    
    if created:
      logger.info(f"Usuario creado: {user.email}")
    else:
      # Si ya existe, actualizar el password (por si cambió el formato del hash)
      user.password = user_data["password"]
      await user.save()
      logger.info(f"Usuario actualizado: {user.email}")
  
  logger.info("Users seeded successfully")