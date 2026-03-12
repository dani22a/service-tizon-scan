import jwt
from src.config import get_jwt_config
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

config = get_jwt_config()

JWT_ALGORITHM = "HS256"

def create_token(user_id: int, email: str) -> str:
  payload = {
    "user_id": user_id,
    "email": email,
    "exp": datetime.now(timezone.utc) + timedelta(seconds=config.JWT_EXPIRATION)
  }
  
  return jwt.encode(payload, config.JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> dict:
  try:
    payload = jwt.decode(token, config.JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return payload
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token has expired")
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=401, detail="Invalid token")

def get_user_id(token: str) -> int:
  payload = verify_token(token)
  return payload["user_id"]

def get_email(token: str) -> str:
  payload = verify_token(token)
  return payload["email"]

def get_payload(token: str) -> dict:
  payload = verify_token(token)
  return payload
