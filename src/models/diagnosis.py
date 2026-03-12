from tortoise import fields

from src.models.base import BaseModel


class DiagnosisReport(BaseModel):
    """
    Snapshot del análisis agregado del cultivo en un momento dado.
    Se genera cada vez que el usuario consulta la vista de diagnóstico.
    """

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="diagnosis_reports",
        on_delete=fields.CASCADE,
    )

    # Métricas generales
    total_evaluaciones = fields.IntField()
    con_clasificacion = fields.IntField()
    sin_clasificacion = fields.IntField()
    confianza_promedio = fields.FloatField()
    total_detecciones = fields.IntField()
    promedio_detecciones_por_imagen = fields.FloatField()
    imagenes_con_blight = fields.IntField()
    tasa_consenso = fields.FloatField()

    # Severidad e índice
    indice_severidad = fields.FloatField(
        description="Porcentaje de muestras con enfermedad (0-100)"
    )
    tendencia = fields.CharField(
        max_length=20,
        description="improving | worsening | stable | unknown",
    )
    clase_reciente = fields.CharField(
        max_length=100,
        null=True,
        description="Última clase predicha, ej: Potato___Late_blight",
    )

    # Distribución por enfermedad (JSON con las stats por clase)
    distribucion_enfermedades = fields.JSONField(
        description=(
            "Dict con count, avgConfidence, avgDetections, "
            "totalBlight, consensusCount por clase"
        ),
        null=True,
    )

    fecha = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "diagnosis_reports"
        ordering = ["-created_at"]


class DiagnosisRecommendation(BaseModel):
    """
    Recomendación generada a partir de un DiagnosisReport.
    Puede almacenar texto libre y metadatos estructurados.
    """

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="diagnosis_recommendations",
        on_delete=fields.CASCADE,
    )
    report = fields.ForeignKeyField(
        "models.DiagnosisReport",
        related_name="recommendations",
        on_delete=fields.CASCADE,
    )

    titulo = fields.CharField(max_length=255, null=True)
    contenido = fields.TextField()
    severidad = fields.CharField(max_length=20, null=True)
    etiquetas = fields.JSONField(null=True)

    fecha = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "diagnosis_recommendations"
        ordering = ["-fecha", "-created_at"]

