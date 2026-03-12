from __future__ import annotations

from src.models.periodo_recommendation import PeriodoReport, PeriodoRecommendation


def _iso(value) -> str | None:
    return value.isoformat() if value else None


def periodo_report_to_dict(
    report: PeriodoReport,
    include_recommendations: bool = True,
) -> dict:
    data: dict = {
        "id": report.id,
        "periodo_id": report.periodo_id,
        # ── métricas generales
        "total_predicciones": report.total_predicciones,
        "con_enfermedad": report.con_enfermedad,
        "saludables": report.saludables,
        "confianza_promedio": report.confianza_promedio,
        "total_detecciones": report.total_detecciones,
        "promedio_detecciones_por_imagen": report.promedio_detecciones_por_imagen,
        "tasa_consenso": report.tasa_consenso,
        # ── métricas temporales
        "dias_activos": report.dias_activos,
        "frecuencia_monitoreo": report.frecuencia_monitoreo,
        # ── severidad / tendencia
        "indice_severidad": report.indice_severidad,
        "tendencia": report.tendencia,
        "enfermedad_predominante": report.enfermedad_predominante,
        # ── cobertura espacial
        "surcos_monitoreados": report.surcos_monitoreados,
        # ── distribución detallada (contexto completo de la recomendación)
        "distribucion_enfermedades": report.distribucion_enfermedades,
        # ── timestamps
        "fecha_reporte": _iso(report.fecha_reporte),
        "created_at": _iso(report.created_at),
        "updated_at": _iso(report.updated_at),
    }

    if include_recommendations:
        recs = getattr(report, "recommendations", None)
        if recs is not None:
            data["recomendaciones"] = [
                periodo_recommendation_to_dict(r, include_report=False)
                for r in recs
            ]

    return data


def periodo_recommendation_to_dict(
    rec: PeriodoRecommendation,
    include_report: bool = True,
) -> dict:
    data: dict = {
        "id": rec.id,
        "periodo_id": rec.periodo_id,
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
                "fecha_reporte": _iso(report.fecha_reporte),
                "indice_severidad": report.indice_severidad,
                "tendencia": report.tendencia,
                "enfermedad_predominante": report.enfermedad_predominante,
                "total_predicciones": report.total_predicciones,
                "con_enfermedad": report.con_enfermedad,
                "confianza_promedio": report.confianza_promedio,
                # snapshot completo para mostrar bajo qué circunstancias se generó
                "distribucion_enfermedades": report.distribucion_enfermedades,
            }

    return data


async def create_periodo_report_with_recommendations(
    user_id: int,
    periodo_id: int,
    payload: dict,
) -> dict:
    """
    Crea un PeriodoReport con sus PeriodoRecommendations asociadas,
    guardando el snapshot completo de métricas para el historial.

    Estructura esperada del payload:
    {
      "total_predicciones": int,
      "con_enfermedad": int,
      "saludables": int,
      "confianza_promedio": float,
      "total_detecciones": int,
      "promedio_detecciones_por_imagen": float,
      "tasa_consenso": float,
      "dias_activos": int,
      "frecuencia_monitoreo": float,
      "indice_severidad": float,
      "tendencia": "mejorando|empeorando|estable|insuficiente_datos",
      "enfermedad_predominante": str | null,
      "surcos_monitoreados": list[int] | null,
      "distribucion_enfermedades": {
        "<clase>": {
          "count": int,
          "pct": float,
          "avgConf": float,
          "avgDets": float,
          "totalBlight": int,
          "consensusCount": int,
          "primera_deteccion": str | null,
          "ultima_deteccion": str | null
        }
      },
      "recomendaciones": [
        {
          "categoria": str,
          "prioridad": str,
          "titulo": str,
          "contenido": str,
          "etiquetas": list[str] | null
        }
      ]
    }
    """
    recomendaciones_data = payload.get("recomendaciones") or []

    report = await PeriodoReport.create(
        usuario_id=user_id,
        periodo_id=periodo_id,
        total_predicciones=payload.get("total_predicciones", 0),
        con_enfermedad=payload.get("con_enfermedad", 0),
        saludables=payload.get("saludables", 0),
        confianza_promedio=payload.get("confianza_promedio", 0.0),
        total_detecciones=payload.get("total_detecciones", 0),
        promedio_detecciones_por_imagen=payload.get(
            "promedio_detecciones_por_imagen", 0.0
        ),
        tasa_consenso=payload.get("tasa_consenso", 0.0),
        dias_activos=payload.get("dias_activos", 0),
        frecuencia_monitoreo=payload.get("frecuencia_monitoreo", 0.0),
        indice_severidad=payload.get("indice_severidad", 0.0),
        tendencia=payload.get("tendencia", "insuficiente_datos"),
        enfermedad_predominante=payload.get("enfermedad_predominante"),
        surcos_monitoreados=payload.get("surcos_monitoreados") or [],
        distribucion_enfermedades=payload.get("distribucion_enfermedades") or {},
    )

    recs_objs: list[PeriodoRecommendation] = []
    for rec_data in recomendaciones_data:
        rec_obj = await PeriodoRecommendation.create(
            usuario_id=user_id,
            periodo_id=periodo_id,
            report=report,
            categoria=rec_data.get("categoria", "general"),
            prioridad=rec_data.get("prioridad", "media"),
            titulo=rec_data.get("titulo", ""),
            contenido=rec_data.get("contenido", ""),
            etiquetas=rec_data.get("etiquetas"),
        )
        recs_objs.append(rec_obj)

    report_dict = periodo_report_to_dict(report, include_recommendations=False)
    report_dict["recomendaciones"] = [
        periodo_recommendation_to_dict(r, include_report=False) for r in recs_objs
    ]
    return report_dict


async def list_periodo_reports(periodo_id: int) -> list[dict]:
    """Retorna todos los reportes (con sus recomendaciones) de un periodo."""
    reports = await (
        PeriodoReport.filter(periodo_id=periodo_id)
        .prefetch_related("recommendations")
        .order_by("-fecha_reporte")
        .all()
    )
    return [periodo_report_to_dict(r, include_recommendations=True) for r in reports]
