from fastapi import APIRouter, Request, HTTPException, Body
from pydantic import BaseModel, Field

from src.services.video_service import (
    create_video_analisis,
    list_video_analisis_by_user,
)
from src.helpers.response import success_response

router = APIRouter()


def _get_user_id(request: Request) -> int:
    return getattr(request.state, "user_id", None) or 1


class VideoAnalisisCreate(BaseModel):
    periodo_id: int | None = Field(None, description="ID de la campaña (periodo)")
    nombre_archivo: str | None = Field(None, description="Nombre original del archivo de video")
    video_url: str | None = Field(None, description="URL o URI del video")
    analysis_payload: dict = Field(..., description="Resultado completo del análisis con Gemini")


@router.post("", status_code=201)
async def create_video(
    request: Request,
    payload: VideoAnalisisCreate = Body(...),
):
    """
    Guarda un análisis de video vinculado opcionalmente a una campaña (periodo).
    El analysis_payload debe contener el resultado completo del análisis con Gemini.
    """
    user_id = _get_user_id(request)
    video = await create_video_analisis(
        user_id=user_id,
        analysis_payload=payload.analysis_payload,
        periodo_id=payload.periodo_id,
        nombre_archivo=payload.nombre_archivo,
        video_url=payload.video_url,
    )
    from src.services.video_service import video_analisis_to_dict
    return success_response(
        await video_analisis_to_dict(video),
        "Análisis de video guardado",
        201,
    )


@router.get("/history", status_code=200)
async def get_video_history(request: Request):
    """Historial de análisis de videos del usuario."""
    user_id = _get_user_id(request)
    videos = await list_video_analisis_by_user(user_id)
    return success_response(videos, "Historial de videos", 200)


