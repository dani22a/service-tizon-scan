import bcrypt

def hash_password(password: str) -> str:
  """
  Hashea un password y devuelve el hash como string (para guardar en DB).
  Usa latin-1 porque los hashes de bcrypt pueden contener bytes no válidos en UTF-8.
  """
  hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  return hashed_bytes.decode('latin-1')

def check_password(password: str, hashed_password: str | bytes) -> bool:
  """
  Verifica un password contra un hash.
  Acepta hash como string o bytes (por si viene de la DB como bytes).
  """
  password_bytes = password.encode('utf-8')
  
  # Si el hash viene como bytes, usarlo directamente
  if isinstance(hashed_password, bytes):
    return bcrypt.checkpw(password_bytes, hashed_password)
  
  # Si viene como string, convertir a bytes usando latin-1 (preserva todos los bytes)
  return bcrypt.checkpw(password_bytes, hashed_password.encode('latin-1'))