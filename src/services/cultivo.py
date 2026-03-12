from __future__ import annotations

from typing import Any

from fastapi import HTTPException

from src.models.lote import Lote
from src.models.modulo import Modulo
from src.models.prediccion import Prediccion
from src.models.surco import Surco
from src.models.user import User
from src.models.classifier import classifier
from src.services.roboflow_service import roboflow_inference_service


def _iso(value: Any) -> str | None:
    return value.isoformat() if value else None


def _validate_modulo_owner(modulo: Modulo, user_id: int) -> None:
    if modulo.user_id != user_id:
        raise HTTPException(status_code=404, detail="Modulo not found")


def _build_fase1_resumen(fase1_payload: dict[str, Any]) -> dict[str, Any]:
    predictions = fase1_payload.get("predictions", []) or []
    clases_detectadas = sorted({prediction.get("class", "") for prediction in predictions if prediction.get("class")})
    return {
        "has_matches": bool(fase1_payload.get("has_matches", False)),
        "total_detecciones": len(predictions),
        "clases_detectadas": clases_detectadas,
    }


def _build_fase2_resumen(fase2_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "clase_predicha": fase2_payload.get("clase_predicha"),
        "confianza": fase2_payload.get("confianza"),
    }


def _modulo_to_dict(modulo: Modulo) -> dict[str, Any]:
    return {
        "id": modulo.id,
        "nombre": modulo.nombre,
        "descripcion": modulo.descripcion,
        "created_at": _iso(modulo.created_at),
        "updated_at": _iso(modulo.updated_at),
    }


def _lote_to_dict(lote: Lote) -> dict[str, Any]:
    return {
        "id": lote.id,
        "modulo_id": lote.modulo_id,
        "identificador": lote.identificador,
        "descripcion": lote.descripcion,
        "created_at": _iso(lote.created_at),
        "updated_at": _iso(lote.updated_at),
    }


def _surco_to_dict(surco: Surco) -> dict[str, Any]:
    return {
        "id": surco.id,
        "lote_id": surco.lote_id,
        "numero": surco.numero,
        "descripcion": surco.descripcion,
        "created_at": _iso(surco.created_at),
        "updated_at": _iso(surco.updated_at),
    }


def _prediccion_to_dict(prediccion: Prediccion) -> dict[str, Any]:
    return {
        "id": prediccion.id,
        "surco_id": prediccion.surco_id,
        "usuario_id": prediccion.usuario_id,
        "imagen_url": prediccion.imagen_url,
        "fase1_resumen": prediccion.fase1_resumen,
        "fase1_payload": prediccion.fase1_payload,
        "fase2_resumen": prediccion.fase2_resumen,
        "fase2_payload": prediccion.fase2_payload,
        "fecha": _iso(prediccion.fecha),
        "created_at": _iso(prediccion.created_at),
        "updated_at": _iso(prediccion.updated_at),
    }


async def list_modulos(user_id: int) -> list[dict[str, Any]]:
    modulos = await Modulo.filter(user_id=user_id).order_by("id")
    return [_modulo_to_dict(modulo) for modulo in modulos]


async def create_modulo(user_id: int, nombre: str, descripcion: str | None) -> dict[str, Any]:
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    modulo = await Modulo.create(user=user, nombre=nombre, descripcion=descripcion)
    return _modulo_to_dict(modulo)


async def get_modulo(user_id: int, modulo_id: int) -> Modulo:
    modulo = await Modulo.get_or_none(id=modulo_id)
    if not modulo:
        raise HTTPException(status_code=404, detail="Modulo not found")

    _validate_modulo_owner(modulo, user_id)
    return modulo


async def get_modulo_detail(user_id: int, modulo_id: int) -> dict[str, Any]:
    modulo = await get_modulo(user_id, modulo_id)
    return _modulo_to_dict(modulo)


async def list_lotes(user_id: int, modulo_id: int) -> list[dict[str, Any]]:
    modulo = await get_modulo(user_id, modulo_id)
    lotes = await Lote.filter(modulo_id=modulo.id).order_by("id")
    return [_lote_to_dict(lote) for lote in lotes]


async def create_lote(user_id: int, modulo_id: int, identificador: str, descripcion: str | None) -> dict[str, Any]:
    modulo = await get_modulo(user_id, modulo_id)

    exists = await Lote.get_or_none(modulo_id=modulo.id, identificador=identificador)
    if exists:
        raise HTTPException(status_code=409, detail="Lote identifier already exists in modulo")

    lote = await Lote.create(modulo=modulo, identificador=identificador, descripcion=descripcion)
    return _lote_to_dict(lote)


async def get_lote(user_id: int, modulo_id: int, lote_id: int) -> Lote:
    modulo = await get_modulo(user_id, modulo_id)
    lote = await Lote.get_or_none(id=lote_id, modulo_id=modulo.id)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote not found")
    return lote


async def list_surcos(user_id: int, modulo_id: int, lote_id: int) -> list[dict[str, Any]]:
    lote = await get_lote(user_id, modulo_id, lote_id)
    surcos = await Surco.filter(lote_id=lote.id).order_by("numero", "id")
    return [_surco_to_dict(surco) for surco in surcos]


async def create_surco(user_id: int, modulo_id: int, lote_id: int, numero: int, descripcion: str | None) -> dict[str, Any]:
    lote = await get_lote(user_id, modulo_id, lote_id)

    exists = await Surco.get_or_none(lote_id=lote.id, numero=numero)
    if exists:
        raise HTTPException(status_code=409, detail="Surco number already exists in lote")

    surco = await Surco.create(lote=lote, numero=numero, descripcion=descripcion)
    return _surco_to_dict(surco)


async def get_surco(user_id: int, modulo_id: int, lote_id: int, surco_id: int) -> Surco:
    lote = await get_lote(user_id, modulo_id, lote_id)
    surco = await Surco.get_or_none(id=surco_id, lote_id=lote.id)
    if not surco:
        raise HTTPException(status_code=404, detail="Surco not found")
    return surco


async def list_predicciones(user_id: int, modulo_id: int, lote_id: int, surco_id: int) -> list[dict[str, Any]]:
    surco = await get_surco(user_id, modulo_id, lote_id, surco_id)
    predicciones = await Prediccion.filter(surco_id=surco.id).order_by("-fecha", "-id")
    return [_prediccion_to_dict(prediccion) for prediccion in predicciones]


async def get_prediccion_detail(
    user_id: int,
    modulo_id: int,
    lote_id: int,
    surco_id: int,
    prediccion_id: int,
) -> dict[str, Any]:
    surco = await get_surco(user_id, modulo_id, lote_id, surco_id)
    prediccion = await Prediccion.get_or_none(id=prediccion_id, surco_id=surco.id)
    if not prediccion:
        raise HTTPException(status_code=404, detail="Prediccion not found")
    return _prediccion_to_dict(prediccion)


async def evaluar_y_guardar_prediccion(
    user_id: int,
    modulo_id: int,
    lote_id: int,
    surco_id: int,
    image_bytes: bytes | None,
    image_url: str | None,
    filename: str | None,
) -> dict[str, Any]:
    surco = await get_surco(user_id, modulo_id, lote_id, surco_id)

    if not image_bytes and not image_url:
        raise HTTPException(status_code=400, detail="Provide either an image file or image_url")

    if image_bytes and image_url:
        raise HTTPException(status_code=400, detail="Provide only one input: file or image_url")

    fase1_payload = await roboflow_inference_service(image_bytes=image_bytes, image_url=image_url)

    if image_bytes:
        fase2_payload = classifier.predict_bytes(image_bytes)
        resolved_image_url = f"uploaded://{filename or 'image'}"
    else:
        raise HTTPException(status_code=400, detail="Fase 2 requires image file upload")

    fase1_resumen = _build_fase1_resumen(fase1_payload)
    fase2_resumen = _build_fase2_resumen(fase2_payload)

    prediccion = await Prediccion.create(
        surco=surco,
        usuario_id=user_id,
        imagen_url=resolved_image_url,
        fase1_resumen=fase1_resumen,
        fase1_payload=fase1_payload,
        fase2_resumen=fase2_resumen,
        fase2_payload=fase2_payload,
    )

    return _prediccion_to_dict(prediccion)
