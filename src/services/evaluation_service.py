from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import Request

from src.models.prediccion import Prediccion
from src.models.surco import Surco
from src.models.diagnosis import DiagnosisReport, DiagnosisRecommendation

PREDICTIONS_DIR = Path(__file__).parent.parent.parent / "public" / "predictions"

_CONTENT_TYPE_EXT = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def _iso(value) -> str | None:
    return value.isoformat() if value else None


def save_image_locally(img_bytes: bytes, content_type: str | None, request: Request) -> str:
    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    ext = _CONTENT_TYPE_EXT.get(content_type or "", ".jpg")
    filename = f"{uuid.uuid4().hex}{ext}"
    (PREDICTIONS_DIR / filename).write_bytes(img_bytes)

    base_url = str(request.base_url).rstrip("/")
    return f"{base_url}/public/predictions/{filename}"


def build_fase1_resumen(fase1_payload: dict) -> dict:
    predictions = fase1_payload.get("predictions", []) or []
    clases = sorted({p.get("class", "") for p in predictions if p.get("class")})
    return {
        "has_matches": bool(fase1_payload.get("has_matches", False)),
        "total_detecciones": len(predictions),
        "clases_detectadas": clases,
    }


def build_fase2_resumen(full_payload: dict) -> dict:
    efficient = full_payload.get("resultados", {}).get("efficient", {})
    return {
        "modelo": "efficient",
        "clase_predicha": efficient.get("clase_predicha"),
        "confianza": efficient.get("confianza"),
    }


def build_fase2_placeholder() -> dict:
    # Keep DB-compatible non-null JSON until phase 2 is completed.
    return {
        "modelo": None,
        "clase_predicha": None,
        "confianza": None,
    }


def build_fase2_payload_placeholder() -> dict:
    # Placeholder structure that matches expected format for fase2_payload
    return {
        "resultados": {
            "efficient": {
                "clase_predicha": None,
                "confianza": None,
            }
        }
    }


async def prediccion_to_dict(p: Prediccion) -> dict:
    # Base fields
    out = {
        "id": p.id,
        "surco_id": p.surco_id,
        "usuario_id": p.usuario_id,
        "periodo_id": p.periodo_id,
        "imagen_url": p.imagen_url,
        "fase1_resumen": p.fase1_resumen,
        "fase1_payload": p.fase1_payload,
        "fase2_resumen": p.fase2_resumen,
        "fase2_payload": p.fase2_payload,
        "fecha": _iso(p.fecha),
        "created_at": _iso(p.created_at),
        "updated_at": _iso(p.updated_at),
    }

    # include related hierarchy info if available
    surco = getattr(p, "surco", None)
    if surco and hasattr(surco, "numero"):
        out["surco_numero"] = surco.numero
        if not hasattr(surco, "lote"):
            await surco.fetch_related("lote")
        lote = surco.lote
        if lote and hasattr(lote, "identificador"):
            out["lote_identificador"] = lote.identificador
            if not hasattr(lote, "modulo"):
                await lote.fetch_related("modulo")
            modulo = lote.modulo
            if modulo and hasattr(modulo, "nombre"):
                out["modulo_nombre"] = modulo.nombre
    return out


async def create_prediccion_fase1(
    user_id: int,
    imagen_url: str,
    fase1_payload: dict,
    surco_id: int | None = None,
    periodo_id: int | None = None,
) -> Prediccion:
    # periodo_id may be None if prediction isn't assigned to any periodo
    return await Prediccion.create(
        usuario_id=user_id,
        imagen_url=imagen_url,
        surco_id=surco_id,
        periodo_id=periodo_id,
        fase1_resumen=build_fase1_resumen(fase1_payload),
        fase1_payload=fase1_payload,
        fase2_resumen=build_fase2_placeholder(),
        fase2_payload=build_fase2_payload_placeholder(),
    )


async def list_predicciones_by_user(user_id: int) -> list[dict]:
    # include related surco/lote/modulo to avoid QuerySet placeholders
    predicciones = await (
        Prediccion.filter(usuario_id=user_id)
        .prefetch_related("surco", "surco__lote", "surco__lote__modulo")
        .order_by("-id")
        .all()
    )
    # convert asynchronously
    result = []
    for p in predicciones:
        result.append(await prediccion_to_dict(p))
    return result


async def update_prediccion_fase2(
    user_id: int,
    fase2_payload: dict,
) -> Prediccion | None:
    # Find the most recent prediction for this user
    # that has fase1_payload but hasn't had fase2 classification results yet
    prediccion = await (
        Prediccion.filter(usuario_id=user_id, fase1_payload__isnull=False)
        .order_by("-id")
        .first()
    )
    if not prediccion:
        return None

    # Use placeholder if fase2_payload is None or empty
    if not fase2_payload:
        fase2_payload = build_fase2_payload_placeholder()

    prediccion.fase2_resumen = build_fase2_resumen(fase2_payload)
    prediccion.fase2_payload = fase2_payload
    await prediccion.save()
    return prediccion


async def list_all_surcos_for_user(user_id: int) -> list[dict]:
    """Get all surcos for a user across all their modules/lotes."""
    # Join: User -> Modulo -> Lote -> Surco
    surcos = await (
        Surco.all()
        .prefetch_related("lote", "lote__modulo", "lote__modulo__user")
        .filter(lote__modulo__user_id=user_id)
        .order_by("lote__modulo__id", "lote__id", "numero")
    )
    
    result = []
    for surco in surcos:
        await surco.fetch_related("lote")
        lote = surco.lote
        await lote.fetch_related("modulo")
        modulo = lote.modulo
        
        result.append({
            "id": surco.id,
            "numero": surco.numero,
            "descripcion": surco.descripcion,
            "lote_id": surco.lote_id,
            "lote_identificador": lote.identificador,
            "modulo_id": modulo.id,
            "modulo_nombre": modulo.nombre,
        })
    
    return result


def diagnosis_report_to_dict(report: DiagnosisReport, include_recommendations: bool = True) -> dict:
    data: dict = {
        "id": report.id,
        "total_evaluaciones": report.total_evaluaciones,
        "con_clasificacion": report.con_clasificacion,
        "sin_clasificacion": report.sin_clasificacion,
        "confianza_promedio": report.confianza_promedio,
        "total_detecciones": report.total_detecciones,
        "promedio_detecciones_por_imagen": report.promedio_detecciones_por_imagen,
        "imagenes_con_blight": report.imagenes_con_blight,
        "tasa_consenso": report.tasa_consenso,
        "indice_severidad": report.indice_severidad,
        "tendencia": report.tendencia,
        "clase_reciente": report.clase_reciente,
        "distribucion_enfermedades": report.distribucion_enfermedades,
        "fecha": _iso(report.fecha),
        "created_at": _iso(report.created_at),
        "updated_at": _iso(report.updated_at),
    }

    if include_recommendations:
        # Prefetched recommendations can be used directly
        recs = getattr(report, "recommendations", None)
        if recs is not None:
            data["recomendaciones"] = [
                recommendation_to_dict(r, include_report=False) for r in recs
            ]

    return data


def recommendation_to_dict(
    rec: DiagnosisRecommendation,
    include_report: bool = True,
) -> dict:
    data: dict = {
        "id": rec.id,
        "titulo": rec.titulo,
        "contenido": rec.contenido,
        "severidad": rec.severidad,
        "etiquetas": rec.etiquetas,
        "fecha": _iso(rec.fecha),
        "created_at": _iso(rec.created_at),
        "updated_at": _iso(rec.updated_at),
    }

    if include_report:
        report = getattr(rec, "report", None)
        if report is not None:
            data["report"] = {
                "id": report.id,
                "fecha": _iso(report.fecha),
                "indice_severidad": report.indice_severidad,
                "tendencia": report.tendencia,
                "clase_reciente": report.clase_reciente,
            }

    return data


async def create_diagnosis_report_with_recommendations(
    user_id: int,
    payload: dict,
) -> dict:
    """
    Crea un DiagnosisReport y las recomendaciones asociadas a partir
    del payload enviado por el frontend.

    Estructura esperada:
    {
      \"total_evaluaciones\": int,
      \"con_clasificacion\": int,
      \"sin_clasificacion\": int,
      \"confianza_promedio\": float,
      \"total_detecciones\": int,
      \"promedio_detecciones_por_imagen\": float,
      \"imagenes_con_blight\": int,
      \"tasa_consenso\": float,
      \"indice_severidad\": float,
      \"tendencia\": \"improving|worsening|stable|unknown\",
      \"clase_reciente\": \"Potato___Late_blight\" | null,
      \"distribucion_enfermedades\": {...},
      \"recomendaciones\": [
        {
          \"titulo\": str | null,
          \"contenido\": str,
          \"severidad\": str | null,
          \"etiquetas\": list[str] | null
        },
        ...
      ]
    }
    """
    recomendaciones_data = payload.get("recomendaciones") or []

    report = await DiagnosisReport.create(
        usuario_id=user_id,
        total_evaluaciones=payload.get("total_evaluaciones", 0),
        con_clasificacion=payload.get("con_clasificacion", 0),
        sin_clasificacion=payload.get("sin_clasificacion", 0),
        confianza_promedio=payload.get("confianza_promedio", 0.0),
        total_detecciones=payload.get("total_detecciones", 0),
        promedio_detecciones_por_imagen=payload.get(
            "promedio_detecciones_por_imagen", 0.0
        ),
        imagenes_con_blight=payload.get("imagenes_con_blight", 0),
        tasa_consenso=payload.get("tasa_consenso", 0.0),
        indice_severidad=payload.get("indice_severidad", 0.0),
        tendencia=payload.get("tendencia", "unknown"),
        clase_reciente=payload.get("clase_reciente"),
        distribucion_enfermedades=payload.get("distribucion_enfermedades") or {},
    )

    recomendaciones_objs: list[DiagnosisRecommendation] = []
    for rec_data in recomendaciones_data:
        rec_obj = await DiagnosisRecommendation.create(
            usuario_id=user_id,
            report=report,
            titulo=rec_data.get("titulo"),
            contenido=rec_data.get("contenido", ""),
            severidad=rec_data.get("severidad"),
            etiquetas=rec_data.get("etiquetas"),
        )
        recomendaciones_objs.append(rec_obj)

    # Serializar reporte + recomendaciones sin asignar al atributo de relación (read-only)
    report_dict = diagnosis_report_to_dict(report, include_recommendations=False)
    report_dict["recomendaciones"] = [
        recommendation_to_dict(r, include_report=False) for r in recomendaciones_objs
    ]
    return report_dict


async def list_recommendations_by_user(user_id: int) -> list[dict]:
    recs = await (
        DiagnosisRecommendation.filter(usuario_id=user_id)
        .prefetch_related("report")
        .order_by("-fecha", "-id")
        .all()
    )
    return [recommendation_to_dict(r, include_report=True) for r in recs]
