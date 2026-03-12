from tortoise import fields

from src.models.base import BaseModel


class PrediccionRecommendation(BaseModel):
    """
    Recomendación generada a partir de una predicción individual.
    Almacena un snapshot de las métricas de la predicción (fase1 y fase2)
    en el momento de la generación, permitiendo historial auditable.
    """

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="prediccion_recommendations",
        on_delete=fields.CASCADE,
    )
    prediccion = fields.ForeignKeyField(
        "models.Prediccion",
        related_name="recommendations",
        on_delete=fields.CASCADE,
    )

    # ── Clasificación ─────────────────────────────────────────────
    categoria = fields.CharField(
        max_length=50,
        description="fungicida | monitoreo | riego | general | alerta",
    )
    prioridad = fields.CharField(
        max_length=20,
        description="urgente | alta | media | baja",
    )

    # ── Contenido ─────────────────────────────────────────────────
    titulo = fields.CharField(max_length=255)
    contenido = fields.TextField()

    # ── Metadatos ─────────────────────────────────────────────────
    etiquetas = fields.JSONField(
        null=True,
        description="Tags como ['late_blight', 'critico', 'preventivo']",
    )

    # ── Snapshot de métricas al momento de la recomendación ───────
    metricas_snapshot = fields.JSONField(
        null=True,
        description=(
            "Snapshot de fase1_resumen, fase2_resumen y contexto espacial "
            "(surco, lote, modulo) al momento de generar la recomendación"
        ),
    )

    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "prediccion_recommendations"
        ordering = ["-fecha_creacion"]
