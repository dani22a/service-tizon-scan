from fastapi import APIRouter, Request, HTTPException, Body
from pydantic import BaseModel, Field
from datetime import date

from src.services import periodo_service
from src.services import periodo_recommendation_service
from src.helpers.response import success_response

router = APIRouter()


class PeriodoCreate(BaseModel):
    nombre: str = Field(..., max_length=255)
    descripcion: str | None = None
    fecha_inicio: date
    fecha_fin: date


def _get_user_id(request: Request) -> int:
    return getattr(request.state, "user_id", None) or 1


@router.post("/periodos", status_code=201)
async def create_periodo(request: Request, body: PeriodoCreate):
    user_id = _get_user_id(request)
    p = await periodo_service.create_periodo(
        user_id=user_id,
        nombre=body.nombre,
        descripcion=body.descripcion,
        fecha_inicio=body.fecha_inicio,
        fecha_fin=body.fecha_fin,
    )
    return success_response(periodo_service.periodo_to_dict(p), "Periodo creado", 201)


@router.get("/periodos", status_code=200)
async def list_periodos(request: Request):
    user_id = _get_user_id(request)
    data = await periodo_service.list_periodos_by_user(user_id)
    return success_response(data, "Periodos obtenidos", 200)


@router.get("/periodos/{periodo_id}", status_code=200)
async def get_periodo(request: Request, periodo_id: int):
    user_id = _get_user_id(request)
    from src.models.periodo import Periodo
    periodo = await Periodo.filter(id=periodo_id, usuario_id=user_id).first()
    if not periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    return success_response(periodo_service.periodo_to_dict(periodo), "Periodo obtenido", 200)


@router.get("/periodos/{periodo_id}/predicciones", status_code=200)
async def get_predicciones_by_periodo(request: Request, periodo_id: int):
    user_id = _get_user_id(request)
    from src.models.periodo import Periodo
    periodo = await Periodo.filter(id=periodo_id, usuario_id=user_id).first()
    if not periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    preds = await periodo_service.list_predicciones_by_periodo(periodo_id)
    return success_response(preds, "Predicciones de periodo", 200)


@router.post("/periodos/{periodo_id}/diagnosis", status_code=201)
async def create_periodo_diagnosis(
    request: Request,
    periodo_id: int,
    payload: dict = Body(...),
):
    """
    Guarda un snapshot de diagnóstico + recomendaciones para un periodo específico.
    El snapshot incluye todas las métricas calculadas, permitiendo ver
    bajo qué circunstancias fue emitida cada recomendación.
    """
    user_id = _get_user_id(request)
    from src.models.periodo import Periodo
    periodo = await Periodo.filter(id=periodo_id, usuario_id=user_id).first()
    if not periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    report = await periodo_recommendation_service.create_periodo_report_with_recommendations(
        user_id=user_id,
        periodo_id=periodo_id,
        payload=payload,
    )
    return success_response(report, "Diagnóstico de periodo guardado", 201)


@router.get("/periodos/{periodo_id}/diagnosis", status_code=200)
async def list_periodo_diagnosis(request: Request, periodo_id: int):
    """
    Retorna todos los reportes históricos de diagnóstico de un periodo,
    cada uno con sus métricas y recomendaciones asociadas.
    """
    user_id = _get_user_id(request)
    from src.models.periodo import Periodo
    periodo = await Periodo.filter(id=periodo_id, usuario_id=user_id).first()
    if not periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    reports = await periodo_recommendation_service.list_periodo_reports(periodo_id)
    return success_response(reports, "Historial de diagnósticos del periodo", 200)
