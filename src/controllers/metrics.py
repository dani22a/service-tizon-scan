import json
from fastapi import APIRouter
from src.constants.general import JSON_PATH
from src.helpers.response import success_response

router = APIRouter()

@router.get("/data", status_code=200)
async def get_metrics():
  with open(JSON_PATH, "r") as f:
    data = json.load(f)
  return success_response(data, message="Metrics retrieved successfully")
