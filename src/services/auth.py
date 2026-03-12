from src.lib.jwt import create_token
from src.models.user import User
from fastapi import HTTPException
from src.lib.bycript import check_password

async def login_service(email: str, password: str):
  user = await User.get_or_none(email=email)

  if not user:
    raise HTTPException(status_code=401, detail="Invalid email or password")
  if not check_password(password, user.password):
    raise HTTPException(status_code=401, detail="Invalid email or password")
  
  token = create_token(user.id, user.email)
  
  return token

async def me_service(user_id: int):
  user = await User.get_or_none(id=user_id)
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  return {
    "id": user.id,
    "username": user.username,
    "email": user.email,
    "full_name": user.full_name,
    "created_at": user.created_at.isoformat() if user.created_at else None,
    "updated_at": user.updated_at.isoformat() if user.updated_at else None,
  }
