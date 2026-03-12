from __future__ import annotations

from src.models.video_analisis import VideoAnalisis


def _iso(value) -> str | None:
    return value.isoformat() if value else None


async def video_analisis_to_dict(v: VideoAnalisis) -> dict:
    out = {
        "id": v.id,
        "usuario_id": v.usuario_id,
        "periodo_id": v.periodo_id,
        "nombre_archivo": v.nombre_archivo,
        "video_url": v.video_url,
        "analysis_payload": v.analysis_payload,
        "fecha": _iso(v.fecha),
        "created_at": _iso(v.created_at),
        "updated_at": _iso(v.updated_at),
    }
    periodo = getattr(v, "periodo", None)
    if periodo and hasattr(periodo, "nombre"):
        out["periodo_nombre"] = periodo.nombre
    return out


async def create_video_analisis(
    user_id: int,
    analysis_payload: dict,
    periodo_id: int | None = None,
    nombre_archivo: str | None = None,
    video_url: str | None = None,
) -> VideoAnalisis:
    return await VideoAnalisis.create(
        usuario_id=user_id,
        periodo_id=periodo_id,
        nombre_archivo=nombre_archivo,
        video_url=video_url,
        analysis_payload=analysis_payload,
    )


async def list_video_analisis_by_user(user_id: int) -> list[dict]:
    videos = await (
        VideoAnalisis.filter(usuario_id=user_id)
        .prefetch_related("periodo")
        .order_by("-id")
        .all()
    )
    return [await video_analisis_to_dict(v) for v in videos]


async def list_video_analisis_by_periodo(periodo_id: int) -> list[dict]:
    videos = await (
        VideoAnalisis.filter(periodo_id=periodo_id)
        .prefetch_related("periodo")
        .order_by("-id")
        .all()
    )
    return [await video_analisis_to_dict(v) for v in videos]
