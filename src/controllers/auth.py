from fastapi import APIRouter, Request
from src.services.auth import login_service, me_service
from src.helpers.response import success_response
from src.helpers.auth import get_current_user_id
from src.schemas.auth import LoginRequest

router = APIRouter()

@router.post("/login", status_code=200)
async def login(body: LoginRequest):
  token = await login_service(body.email, body.password)
  return success_response({"token": token}, "Login successful", status_code=200)

@router.post("/logout", status_code=200)
async def logout(request: Request):
  _ = get_current_user_id(request)
  return success_response(None, "Logout successful", status_code=200)

@router.get("/me", status_code=200)
async def me(request: Request):
  user_id = get_current_user_id(request)
  user = await me_service(user_id)
  return success_response(user, "User fetched successfully", status_code=200)
