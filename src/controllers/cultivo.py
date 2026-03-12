from fastapi import APIRouter, Body, File, Form, HTTPException, Request, UploadFile

from src.helpers.auth import get_current_user_id
from src.helpers.response import success_response
from src.schemas.cultivo import LoteCreate, ModuloCreate, SurcoCreate
from src.services.cultivo import (
    create_lote,
    create_modulo,
    create_surco,
    evaluar_y_guardar_prediccion,
    get_modulo_detail,
    get_prediccion_detail,
    list_lotes,
    list_modulos,
    list_predicciones,
    list_surcos,
)
from src.services import spatial_recommendation_service
from src.services.roboflow_service import validate_image_content_type

router = APIRouter()


@router.get("", status_code=200)
async def obtener_modulos(request: Request):
    user_id = get_current_user_id(request)
    modulos = await list_modulos(user_id)
    return success_response(modulos, "Modulos fetched successfully", status_code=200)


@router.post("", status_code=201)
async def crear_modulo(body: ModuloCreate, request: Request):
    user_id = get_current_user_id(request)
    modulo = await create_modulo(user_id, body.nombre, body.descripcion)
    return success_response(modulo, "Modulo created successfully", status_code=201)


@router.get("/{modulo_id}", status_code=200)
async def obtener_modulo(modulo_id: int, request: Request):
    user_id = get_current_user_id(request)
    modulo = await get_modulo_detail(user_id, modulo_id)
    return success_response(modulo, "Modulo fetched successfully", status_code=200)


@router.get("/{modulo_id}/lotes", status_code=200)
async def obtener_lotes(modulo_id: int, request: Request):
    user_id = get_current_user_id(request)
    lotes = await list_lotes(user_id, modulo_id)
    return success_response(lotes, "Lotes fetched successfully", status_code=200)


@router.post("/{modulo_id}/lotes", status_code=201)
async def crear_lote(modulo_id: int, body: LoteCreate, request: Request):
    user_id = get_current_user_id(request)
    lote = await create_lote(user_id, modulo_id, body.identificador, body.descripcion)
    return success_response(lote, "Lote created successfully", status_code=201)


@router.get("/{modulo_id}/lotes/{lote_id}/surcos", status_code=200)
async def obtener_surcos(modulo_id: int, lote_id: int, request: Request):
    user_id = get_current_user_id(request)
    surcos = await list_surcos(user_id, modulo_id, lote_id)
    return success_response(surcos, "Surcos fetched successfully", status_code=200)


@router.post("/{modulo_id}/lotes/{lote_id}/surcos", status_code=201)
async def crear_surco(modulo_id: int, lote_id: int, body: SurcoCreate, request: Request):
    user_id = get_current_user_id(request)
    surco = await create_surco(user_id, modulo_id, lote_id, body.numero, body.descripcion)
    return success_response(surco, "Surco created successfully", status_code=201)


@router.get("/{modulo_id}/lotes/{lote_id}/surcos/{surco_id}/predicciones", status_code=200)
async def obtener_predicciones(modulo_id: int, lote_id: int, surco_id: int, request: Request):
    user_id = get_current_user_id(request)
    predicciones = await list_predicciones(user_id, modulo_id, lote_id, surco_id)
    return success_response(predicciones, "Predicciones fetched successfully", status_code=200)


@router.get("/{modulo_id}/lotes/{lote_id}/surcos/{surco_id}/predicciones/{prediccion_id}", status_code=200)
async def obtener_prediccion(
    modulo_id: int,
    lote_id: int,
    surco_id: int,
    prediccion_id: int,
    request: Request,
):
    user_id = get_current_user_id(request)
    prediccion = await get_prediccion_detail(user_id, modulo_id, lote_id, surco_id, prediccion_id)
    return success_response(prediccion, "Prediccion fetched successfully", status_code=200)


@router.post("/{modulo_id}/lotes/{lote_id}/surcos/{surco_id}/predicciones/evaluar", status_code=201)
async def evaluar_surco(
    modulo_id: int,
    lote_id: int,
    surco_id: int,
    request: Request,
    file: UploadFile | None = File(None),
    image_url: str | None = Form(None),
):
    user_id = get_current_user_id(request)

    image_bytes: bytes | None = None
    if file:
        validate_image_content_type(file.content_type)
        image_bytes = await file.read()

    prediccion = await evaluar_y_guardar_prediccion(
        user_id=user_id,
        modulo_id=modulo_id,
        lote_id=lote_id,
        surco_id=surco_id,
        image_bytes=image_bytes,
        image_url=image_url,
        filename=file.filename if file else None,
    )

    return success_response(prediccion, "Prediccion created successfully", status_code=201)


# ── Diagnóstico espacial ──────────────────────────────────────────

@router.post("/{modulo_id}/lotes/{lote_id}/surcos/{surco_id}/diagnosis", status_code=201)
async def crear_surco_diagnosis(
    modulo_id: int,
    lote_id: int,
    surco_id: int,
    request: Request,
    payload: dict = Body(...),
):
    """
    Guarda un snapshot de diagnóstico + recomendaciones para un surco específico.

    Payload:
    {
      "total_predicciones": int,
      "con_enfermedad": int,
      "saludables": int,
      "confianza_promedio": float,
      "total_detecciones": int,
      "promedio_detecciones_por_imagen": float,
      "tasa_consenso": float,
      "indice_severidad": float,
      "tendencia": "mejorando|empeorando|estable|insuficiente_datos",
      "enfermedad_predominante": str | null,
      "distribucion_enfermedades": {...} | null,
      "recomendaciones": [{"categoria", "prioridad", "titulo", "contenido", "etiquetas"}]
    }
    """
    user_id = get_current_user_id(request)
    from src.models.surco import Surco
    surco = await Surco.filter(
        id=surco_id, lote_id=lote_id, lote__modulo_id=modulo_id
    ).prefetch_related("lote__modulo").first()
    if not surco or surco.lote.modulo.user_id != user_id:
        raise HTTPException(status_code=404, detail="Surco no encontrado")
    report = await spatial_recommendation_service.create_surco_report_with_recommendations(
        user_id=user_id,
        surco_id=surco_id,
        payload=payload,
    )
    return success_response(report, "Diagnóstico de surco guardado", status_code=201)


@router.get("/{modulo_id}/lotes/{lote_id}/surcos/{surco_id}/diagnosis", status_code=200)
async def listar_surco_diagnosis(
    modulo_id: int,
    lote_id: int,
    surco_id: int,
    request: Request,
):
    """Retorna el historial de diagnósticos de un surco."""
    user_id = get_current_user_id(request)
    from src.models.surco import Surco
    surco = await Surco.filter(
        id=surco_id, lote_id=lote_id, lote__modulo_id=modulo_id
    ).prefetch_related("lote__modulo").first()
    if not surco or surco.lote.modulo.user_id != user_id:
        raise HTTPException(status_code=404, detail="Surco no encontrado")
    reports = await spatial_recommendation_service.list_surco_reports(surco_id)
    return success_response(reports, "Historial de diagnósticos del surco", status_code=200)


@router.post("/{modulo_id}/lotes/{lote_id}/diagnosis", status_code=201)
async def crear_lote_diagnosis(
    modulo_id: int,
    lote_id: int,
    request: Request,
    payload: dict = Body(...),
):
    """
    Guarda un snapshot de diagnóstico + recomendaciones para un lote.
    Agrega métricas de todos los surcos del lote.

    Payload: mismos campos base + "surcos_monitoreados": list[int] | null
    """
    user_id = get_current_user_id(request)
    from src.models.lote import Lote
    lote = await Lote.filter(id=lote_id, modulo_id=modulo_id).prefetch_related("modulo").first()
    if not lote or lote.modulo.user_id != user_id:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    report = await spatial_recommendation_service.create_lote_report_with_recommendations(
        user_id=user_id,
        lote_id=lote_id,
        payload=payload,
    )
    return success_response(report, "Diagnóstico de lote guardado", status_code=201)


@router.get("/{modulo_id}/lotes/{lote_id}/diagnosis", status_code=200)
async def listar_lote_diagnosis(
    modulo_id: int,
    lote_id: int,
    request: Request,
):
    """Retorna el historial de diagnósticos de un lote."""
    user_id = get_current_user_id(request)
    from src.models.lote import Lote
    lote = await Lote.filter(id=lote_id, modulo_id=modulo_id).prefetch_related("modulo").first()
    if not lote or lote.modulo.user_id != user_id:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    reports = await spatial_recommendation_service.list_lote_reports(lote_id)
    return success_response(reports, "Historial de diagnósticos del lote", status_code=200)


@router.post("/{modulo_id}/diagnosis", status_code=201)
async def crear_modulo_diagnosis(
    modulo_id: int,
    request: Request,
    payload: dict = Body(...),
):
    """
    Guarda un snapshot de diagnóstico + recomendaciones para un módulo completo.
    Agrega métricas de todos los lotes y surcos del módulo.

    Payload: mismos campos base + "lotes_monitoreados": list[int] | null
                                  + "surcos_monitoreados": list[int] | null
    """
    user_id = get_current_user_id(request)
    from src.models.modulo import Modulo
    modulo = await Modulo.filter(id=modulo_id, user_id=user_id).first()
    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    report = await spatial_recommendation_service.create_modulo_report_with_recommendations(
        user_id=user_id,
        modulo_id=modulo_id,
        payload=payload,
    )
    return success_response(report, "Diagnóstico de módulo guardado", status_code=201)


@router.get("/{modulo_id}/diagnosis", status_code=200)
async def listar_modulo_diagnosis(
    modulo_id: int,
    request: Request,
):
    """Retorna el historial de diagnósticos de un módulo."""
    user_id = get_current_user_id(request)
    from src.models.modulo import Modulo
    modulo = await Modulo.filter(id=modulo_id, user_id=user_id).first()
    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    reports = await spatial_recommendation_service.list_modulo_reports(modulo_id)
    return success_response(reports, "Historial de diagnósticos del módulo", status_code=200)
