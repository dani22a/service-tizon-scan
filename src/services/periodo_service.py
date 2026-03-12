from __future__ import annotations

from typing import List

from src.models.periodo import Periodo
from src.models.prediccion import Prediccion


def periodo_to_dict(p: Periodo) -> dict:
    return {
        "id": p.id,
        "nombre": p.nombre,
        "descripcion": p.descripcion,
        "fecha_inicio": p.fecha_inicio.isoformat() if p.fecha_inicio else None,
        "fecha_fin": p.fecha_fin.isoformat() if p.fecha_fin else None,
        "usuario_id": p.usuario_id,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }


async def create_periodo(
    user_id: int,
    nombre: str,
    fecha_inicio,
    fecha_fin,
    descripcion: str | None = None,
) -> Periodo:
    return await Periodo.create(
        usuario_id=user_id,
        nombre=nombre,
        descripcion=descripcion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )


async def list_periodos_by_user(user_id: int) -> list[dict]:
    periodos = await Periodo.filter(usuario_id=user_id).order_by("-fecha_inicio").all()
    return [periodo_to_dict(p) for p in periodos]


async def list_predicciones_by_periodo(periodo_id: int) -> list[dict]:
    preds = await (
        Prediccion.filter(periodo_id=periodo_id)
        .prefetch_related("surco", "surco__lote", "surco__lote__modulo")
        .order_by("-id")
        .all()
    )
    # reuse evaluation_service prediccion_to_dict to avoid import cycle? We'll import here.
    from src.services.evaluation_service import prediccion_to_dict
    result = []
    for p in preds:
        result.append(await prediccion_to_dict(p))
    return result
