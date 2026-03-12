from __future__ import annotations

from src.models.prediction_recommendation import PrediccionRecommendation
from src.models.prediccion import Prediccion


def _iso(value) -> str | None:
    return value.isoformat() if value else None


def prediccion_recommendation_to_dict(
    rec: PrediccionRecommendation,
    include_prediccion: bool = False,
) -> dict:
    data: dict = {
        "id": rec.id,
        "prediccion_id": rec.prediccion_id,
        "usuario_id": rec.usuario_id,
        "categoria": rec.categoria,
        "prioridad": rec.prioridad,
        "titulo": rec.titulo,
        "contenido": rec.contenido,
        "etiquetas": rec.etiquetas,
        "metricas_snapshot": rec.metricas_snapshot,
        "fecha_creacion": _iso(rec.fecha_creacion),
        "created_at": _iso(rec.created_at),
        "updated_at": _iso(rec.updated_at),
    }
    if include_prediccion:
        prediccion = getattr(rec, "prediccion", None)
        if prediccion is not None:
            data["prediccion"] = {
                "id": prediccion.id,
                "imagen_url": prediccion.imagen_url,
                "fase1_resumen": prediccion.fase1_resumen,
                "fase2_resumen": prediccion.fase2_resumen,
                "fecha": _iso(prediccion.fecha),
            }
    return data


async def create_prediccion_recommendation(
    user_id: int,
    prediccion_id: int,
    payload: dict,
) -> dict:
    """
    Crea una PrediccionRecommendation con el snapshot de métricas de la predicción.

    Estructura esperada del payload:
    {
      "categoria": str,           # "fungicida" | "monitoreo" | "riego" | "general" | "alerta"
      "prioridad": str,           # "urgente" | "alta" | "media" | "baja"
      "titulo": str,
      "contenido": str,
      "etiquetas": list[str] | null,
      "metricas_snapshot": {      # snapshot capturado por el frontend al momento de generar
        "fase1_resumen": {...} | null,
        "fase2_resumen": {...} | null,
        "surco_id": int | null,
        "surco_numero": int | null,
        "lote_identificador": str | null,
        "modulo_nombre": str | null
      } | null
    }
    """
    rec = await PrediccionRecommendation.create(
        usuario_id=user_id,
        prediccion_id=prediccion_id,
        categoria=payload.get("categoria", "general"),
        prioridad=payload.get("prioridad", "media"),
        titulo=payload.get("titulo", ""),
        contenido=payload.get("contenido", ""),
        etiquetas=payload.get("etiquetas"),
        metricas_snapshot=payload.get("metricas_snapshot"),
    )
    return prediccion_recommendation_to_dict(rec)


async def list_prediccion_recommendations(prediccion_id: int) -> list[dict]:
    """Retorna todas las recomendaciones históricas de una predicción."""
    recs = await (
        PrediccionRecommendation.filter(prediccion_id=prediccion_id)
        .order_by("-fecha_creacion")
        .all()
    )
    return [prediccion_recommendation_to_dict(r) for r in recs]


async def get_latest_prediccion_recommendation(prediccion_id: int) -> dict | None:
    """Retorna la recomendación más reciente de una predicción."""
    rec = await (
        PrediccionRecommendation.filter(prediccion_id=prediccion_id)
        .order_by("-fecha_creacion")
        .first()
    )
    return prediccion_recommendation_to_dict(rec) if rec else None
