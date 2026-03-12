from tortoise import fields

from src.models.base import BaseModel


class VideoAnalisis(BaseModel):
    """Análisis de video con Gemini vinculado a una campaña (periodo)."""

    usuario = fields.ForeignKeyField(
        "models.User", related_name="video_analisis", on_delete=fields.CASCADE
    )
    periodo = fields.ForeignKeyField(
        "models.Periodo",
        related_name="video_analisis",
        on_delete=fields.SET_NULL,
        null=True,
    )
    nombre_archivo = fields.CharField(max_length=255, null=True)
    video_url = fields.TextField(null=True)
    analysis_payload = fields.JSONField()
    fecha = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "video_analisis"
