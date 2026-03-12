from __future__ import annotations

from src.models.spatial_recommendation import (
    SurcoReport,
    SurcoRecommendation,
    LoteReport,
    LoteRecommendation,
    ModuloReport,
    ModuloRecommendation,
)


def _iso(value) -> str | None:
    return value.isoformat() if value else None


# ═══════════════════════════════════════════════════════════════════
#  Helpers de serialización — Surco
# ═══════════════════════════════════════════════════════════════════

def surco_report_to_dict(report: SurcoReport, include_recommendations: bool = True) -> dict:
    data: dict = {
        "id": report.id,
        "surco_id": report.surco_id,
        "usuario_id": report.usuario_id,
        "total_predicciones": report.total_predicciones,
        "con_enfermedad": report.con_enfermedad,
        "saludables": report.saludables,
        "confianza_promedio": report.confianza_promedio,
        "total_detecciones": report.total_detecciones,
        "promedio_detecciones_por_imagen": report.promedio_detecciones_por_imagen,
        "tasa_consenso": report.tasa_consenso,
        "indice_severidad": report.indice_severidad,
        "tendencia": report.tendencia,
        "enfermedad_predominante": report.enfermedad_predominante,
        "distribucion_enfermedades": report.distribucion_enfermedades,
        "fecha_reporte": _iso(report.fecha_reporte),
        "created_at": _iso(report.created_at),
        "updated_at": _iso(report.updated_at),
    }
    if include_recommendations:
        recs = getattr(report, "recommendations", None)
        if recs is not None:
            data["recomendaciones"] = [
                surco_recommendation_to_dict(r, include_report=False) for r in recs
            ]
    return data


def surco_recommendation_to_dict(rec: SurcoRecommendation, include_report: bool = True) -> dict:
    data: dict = {
        "id": rec.id,
        "surco_id": rec.surco_id,
        "report_id": rec.report_id,
        "categoria": rec.categoria,
        "prioridad": rec.prioridad,
        "titulo": rec.titulo,
        "contenido": rec.contenido,
        "etiquetas": rec.etiquetas,
        "fecha_creacion": _iso(rec.fecha_creacion),
        "created_at": _iso(rec.created_at),
        "updated_at": _iso(rec.updated_at),
    }
    if include_report:
        report = getattr(rec, "report", None)
        if report is not None:
            data["report"] = {
                "id": report.id,
                "surco_id": report.surco_id,
                "fecha_reporte": _iso(report.fecha_reporte),
                "indice_severidad": report.indice_severidad,
                "tendencia": report.tendencia,
                "enfermedad_predominante": report.enfermedad_predominante,
                "total_predicciones": report.total_predicciones,
                "con_enfermedad": report.con_enfermedad,
                "confianza_promedio": report.confianza_promedio,
            }
    return data


# ═══════════════════════════════════════════════════════════════════
#  Helpers de serialización — Lote
# ═══════════════════════════════════════════════════════════════════

def lote_report_to_dict(report: LoteReport, include_recommendations: bool = True) -> dict:
    data: dict = {
        "id": report.id,
        "lote_id": report.lote_id,
        "usuario_id": report.usuario_id,
        "total_predicciones": report.total_predicciones,
        "con_enfermedad": report.con_enfermedad,
        "saludables": report.saludables,
        "confianza_promedio": report.confianza_promedio,
        "total_detecciones": report.total_detecciones,
        "promedio_detecciones_por_imagen": report.promedio_detecciones_por_imagen,
        "tasa_consenso": report.tasa_consenso,
        "indice_severidad": report.indice_severidad,
        "tendencia": report.tendencia,
        "enfermedad_predominante": report.enfermedad_predominante,
        "surcos_monitoreados": report.surcos_monitoreados,
        "distribucion_enfermedades": report.distribucion_enfermedades,
        "fecha_reporte": _iso(report.fecha_reporte),
        "created_at": _iso(report.created_at),
        "updated_at": _iso(report.updated_at),
    }
    if include_recommendations:
        recs = getattr(report, "recommendations", None)
        if recs is not None:
            data["recomendaciones"] = [
                lote_recommendation_to_dict(r, include_report=False) for r in recs
            ]
    return data


def lote_recommendation_to_dict(rec: LoteRecommendation, include_report: bool = True) -> dict:
    data: dict = {
        "id": rec.id,
        "lote_id": rec.lote_id,
        "report_id": rec.report_id,
        "categoria": rec.categoria,
        "prioridad": rec.prioridad,
        "titulo": rec.titulo,
        "contenido": rec.contenido,
        "etiquetas": rec.etiquetas,
        "fecha_creacion": _iso(rec.fecha_creacion),
        "created_at": _iso(rec.created_at),
        "updated_at": _iso(rec.updated_at),
    }
    if include_report:
        report = getattr(rec, "report", None)
        if report is not None:
            data["report"] = {
                "id": report.id,
                "lote_id": report.lote_id,
                "fecha_reporte": _iso(report.fecha_reporte),
                "indice_severidad": report.indice_severidad,
                "tendencia": report.tendencia,
                "enfermedad_predominante": report.enfermedad_predominante,
                "total_predicciones": report.total_predicciones,
                "con_enfermedad": report.con_enfermedad,
                "confianza_promedio": report.confianza_promedio,
                "surcos_monitoreados": report.surcos_monitoreados,
            }
    return data


# ═══════════════════════════════════════════════════════════════════
#  Helpers de serialización — Módulo
# ═══════════════════════════════════════════════════════════════════

def modulo_report_to_dict(report: ModuloReport, include_recommendations: bool = True) -> dict:
    data: dict = {
        "id": report.id,
        "modulo_id": report.modulo_id,
        "usuario_id": report.usuario_id,
        "total_predicciones": report.total_predicciones,
        "con_enfermedad": report.con_enfermedad,
        "saludables": report.saludables,
        "confianza_promedio": report.confianza_promedio,
        "total_detecciones": report.total_detecciones,
        "promedio_detecciones_por_imagen": report.promedio_detecciones_por_imagen,
        "tasa_consenso": report.tasa_consenso,
        "indice_severidad": report.indice_severidad,
        "tendencia": report.tendencia,
        "enfermedad_predominante": report.enfermedad_predominante,
        "lotes_monitoreados": report.lotes_monitoreados,
        "surcos_monitoreados": report.surcos_monitoreados,
        "distribucion_enfermedades": report.distribucion_enfermedades,
        "fecha_reporte": _iso(report.fecha_reporte),
        "created_at": _iso(report.created_at),
        "updated_at": _iso(report.updated_at),
    }
    if include_recommendations:
        recs = getattr(report, "recommendations", None)
        if recs is not None:
            data["recomendaciones"] = [
                modulo_recommendation_to_dict(r, include_report=False) for r in recs
            ]
    return data


def modulo_recommendation_to_dict(rec: ModuloRecommendation, include_report: bool = True) -> dict:
    data: dict = {
        "id": rec.id,
        "modulo_id": rec.modulo_id,
        "report_id": rec.report_id,
        "categoria": rec.categoria,
        "prioridad": rec.prioridad,
        "titulo": rec.titulo,
        "contenido": rec.contenido,
        "etiquetas": rec.etiquetas,
        "fecha_creacion": _iso(rec.fecha_creacion),
        "created_at": _iso(rec.created_at),
        "updated_at": _iso(rec.updated_at),
    }
    if include_report:
        report = getattr(rec, "report", None)
        if report is not None:
            data["report"] = {
                "id": report.id,
                "modulo_id": report.modulo_id,
                "fecha_reporte": _iso(report.fecha_reporte),
                "indice_severidad": report.indice_severidad,
                "tendencia": report.tendencia,
                "enfermedad_predominante": report.enfermedad_predominante,
                "total_predicciones": report.total_predicciones,
                "con_enfermedad": report.con_enfermedad,
                "confianza_promedio": report.confianza_promedio,
                "lotes_monitoreados": report.lotes_monitoreados,
                "surcos_monitoreados": report.surcos_monitoreados,
            }
    return data


# ═══════════════════════════════════════════════════════════════════
#  CRUD — Surco
# ═══════════════════════════════════════════════════════════════════

async def create_surco_report_with_recommendations(
    user_id: int,
    surco_id: int,
    payload: dict,
) -> dict:
    """
    Crea un SurcoReport con sus SurcoRecommendations asociadas.

    Estructura esperada del payload:
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
      "recomendaciones": [
        {"categoria": str, "prioridad": str, "titulo": str, "contenido": str, "etiquetas": list | null}
      ]
    }
    """
    recomendaciones_data = payload.get("recomendaciones") or []
    report = await SurcoReport.create(
        usuario_id=user_id,
        surco_id=surco_id,
        total_predicciones=payload.get("total_predicciones", 0),
        con_enfermedad=payload.get("con_enfermedad", 0),
        saludables=payload.get("saludables", 0),
        confianza_promedio=payload.get("confianza_promedio", 0.0),
        total_detecciones=payload.get("total_detecciones", 0),
        promedio_detecciones_por_imagen=payload.get("promedio_detecciones_por_imagen", 0.0),
        tasa_consenso=payload.get("tasa_consenso", 0.0),
        indice_severidad=payload.get("indice_severidad", 0.0),
        tendencia=payload.get("tendencia", "insuficiente_datos"),
        enfermedad_predominante=payload.get("enfermedad_predominante"),
        distribucion_enfermedades=payload.get("distribucion_enfermedades") or {},
    )
    recs_objs: list[SurcoRecommendation] = []
    for rec_data in recomendaciones_data:
        rec_obj = await SurcoRecommendation.create(
            usuario_id=user_id,
            surco_id=surco_id,
            report=report,
            categoria=rec_data.get("categoria", "general"),
            prioridad=rec_data.get("prioridad", "media"),
            titulo=rec_data.get("titulo", ""),
            contenido=rec_data.get("contenido", ""),
            etiquetas=rec_data.get("etiquetas"),
        )
        recs_objs.append(rec_obj)

    result = surco_report_to_dict(report, include_recommendations=False)
    result["recomendaciones"] = [
        surco_recommendation_to_dict(r, include_report=False) for r in recs_objs
    ]
    return result


async def list_surco_reports(surco_id: int) -> list[dict]:
    reports = await (
        SurcoReport.filter(surco_id=surco_id)
        .prefetch_related("recommendations")
        .order_by("-fecha_reporte")
        .all()
    )
    return [surco_report_to_dict(r) for r in reports]


# ═══════════════════════════════════════════════════════════════════
#  CRUD — Lote
# ═══════════════════════════════════════════════════════════════════

async def create_lote_report_with_recommendations(
    user_id: int,
    lote_id: int,
    payload: dict,
) -> dict:
    """
    Crea un LoteReport con sus LoteRecommendations asociadas.

    Mismos campos base que SurcoReport más:
      "surcos_monitoreados": list[int] | null
    """
    recomendaciones_data = payload.get("recomendaciones") or []
    report = await LoteReport.create(
        usuario_id=user_id,
        lote_id=lote_id,
        total_predicciones=payload.get("total_predicciones", 0),
        con_enfermedad=payload.get("con_enfermedad", 0),
        saludables=payload.get("saludables", 0),
        confianza_promedio=payload.get("confianza_promedio", 0.0),
        total_detecciones=payload.get("total_detecciones", 0),
        promedio_detecciones_por_imagen=payload.get("promedio_detecciones_por_imagen", 0.0),
        tasa_consenso=payload.get("tasa_consenso", 0.0),
        indice_severidad=payload.get("indice_severidad", 0.0),
        tendencia=payload.get("tendencia", "insuficiente_datos"),
        enfermedad_predominante=payload.get("enfermedad_predominante"),
        surcos_monitoreados=payload.get("surcos_monitoreados") or [],
        distribucion_enfermedades=payload.get("distribucion_enfermedades") or {},
    )
    recs_objs: list[LoteRecommendation] = []
    for rec_data in recomendaciones_data:
        rec_obj = await LoteRecommendation.create(
            usuario_id=user_id,
            lote_id=lote_id,
            report=report,
            categoria=rec_data.get("categoria", "general"),
            prioridad=rec_data.get("prioridad", "media"),
            titulo=rec_data.get("titulo", ""),
            contenido=rec_data.get("contenido", ""),
            etiquetas=rec_data.get("etiquetas"),
        )
        recs_objs.append(rec_obj)

    result = lote_report_to_dict(report, include_recommendations=False)
    result["recomendaciones"] = [
        lote_recommendation_to_dict(r, include_report=False) for r in recs_objs
    ]
    return result


async def list_lote_reports(lote_id: int) -> list[dict]:
    reports = await (
        LoteReport.filter(lote_id=lote_id)
        .prefetch_related("recommendations")
        .order_by("-fecha_reporte")
        .all()
    )
    return [lote_report_to_dict(r) for r in reports]


# ═══════════════════════════════════════════════════════════════════
#  CRUD — Módulo
# ═══════════════════════════════════════════════════════════════════

async def create_modulo_report_with_recommendations(
    user_id: int,
    modulo_id: int,
    payload: dict,
) -> dict:
    """
    Crea un ModuloReport con sus ModuloRecommendations asociadas.

    Mismos campos base más:
      "lotes_monitoreados": list[int] | null,
      "surcos_monitoreados": list[int] | null
    """
    recomendaciones_data = payload.get("recomendaciones") or []
    report = await ModuloReport.create(
        usuario_id=user_id,
        modulo_id=modulo_id,
        total_predicciones=payload.get("total_predicciones", 0),
        con_enfermedad=payload.get("con_enfermedad", 0),
        saludables=payload.get("saludables", 0),
        confianza_promedio=payload.get("confianza_promedio", 0.0),
        total_detecciones=payload.get("total_detecciones", 0),
        promedio_detecciones_por_imagen=payload.get("promedio_detecciones_por_imagen", 0.0),
        tasa_consenso=payload.get("tasa_consenso", 0.0),
        indice_severidad=payload.get("indice_severidad", 0.0),
        tendencia=payload.get("tendencia", "insuficiente_datos"),
        enfermedad_predominante=payload.get("enfermedad_predominante"),
        lotes_monitoreados=payload.get("lotes_monitoreados") or [],
        surcos_monitoreados=payload.get("surcos_monitoreados") or [],
        distribucion_enfermedades=payload.get("distribucion_enfermedades") or {},
    )
    recs_objs: list[ModuloRecommendation] = []
    for rec_data in recomendaciones_data:
        rec_obj = await ModuloRecommendation.create(
            usuario_id=user_id,
            modulo_id=modulo_id,
            report=report,
            categoria=rec_data.get("categoria", "general"),
            prioridad=rec_data.get("prioridad", "media"),
            titulo=rec_data.get("titulo", ""),
            contenido=rec_data.get("contenido", ""),
            etiquetas=rec_data.get("etiquetas"),
        )
        recs_objs.append(rec_obj)

    result = modulo_report_to_dict(report, include_recommendations=False)
    result["recomendaciones"] = [
        modulo_recommendation_to_dict(r, include_report=False) for r in recs_objs
    ]
    return result


async def list_modulo_reports(modulo_id: int) -> list[dict]:
    reports = await (
        ModuloReport.filter(modulo_id=modulo_id)
        .prefetch_related("recommendations")
        .order_by("-fecha_reporte")
        .all()
    )
    return [modulo_report_to_dict(r) for r in reports]
