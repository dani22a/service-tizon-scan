from fastapi import APIRouter
from src.constants.general import HISTORY_PATH
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/history", status_code=200)
async def history():
  return FileResponse(HISTORY_PATH)