from tortoise import fields

from src.models.base import BaseModel


class PeriodoReport(BaseModel):
    """
    Snapshot del análisis agregado de un periodo específico.
    Se genera cuando el usuario guarda el diagnóstico de un periodo.
    Almacena todas las métricas para justificar las recomendaciones emitidas.
    """

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="periodo_reports",
        on_delete=fields.CASCADE,
    )
    periodo = fields.ForeignKeyField(
        "models.Periodo",
        related_name="reports",
        on_delete=fields.CASCADE,
    )

    # ── Métricas generales ───────────────────────────────────────
    total_predicciones = fields.IntField()
    con_enfermedad = fields.IntField()
    saludables = fields.IntField()
    confianza_promedio = fields.FloatField()
    total_detecciones = fields.IntField()
    promedio_detecciones_por_imagen = fields.FloatField()
    tasa_consenso = fields.FloatField()

    # ── Métricas temporales ──────────────────────────────────────
    dias_activos = fields.IntField(
        description="Días del periodo con al menos 1 predicción"
    )
    frecuencia_monitoreo = fields.FloatField(
        description="Predicciones por día promedio"
    )

    # ── Severidad e índice ───────────────────────────────────────
    indice_severidad = fields.FloatField(
        description="Porcentaje de predicciones con enfermedad (0-100)"
    )

    # ── Tendencia dentro del periodo ─────────────────────────────
    tendencia = fields.CharField(
        max_length=30,
        description="mejorando | empeorando | estable | insuficiente_datos",
    )

    # ── Enfermedad predominante ──────────────────────────────────
    enfermedad_predominante = fields.CharField(
        max_length=100,
        null=True,
        description="Clase de enfermedad más frecuente en el periodo",
    )

    # ── Cobertura espacial ───────────────────────────────────────
    surcos_monitoreados = fields.JSONField(
        null=True,
        description="Lista de IDs de surcos evaluados",
    )

    # ── Distribución detallada por enfermedad ────────────────────
    distribucion_enfermedades = fields.JSONField(
        null=True,
        description=(
            "Dict por clase con count, pct, avgConf, avgDets, "
            "totalBlight, consensusCount, primera_deteccion, ultima_deteccion"
        ),
    )

    fecha_reporte = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "periodo_reports"
        ordering = ["-fecha_reporte"]


class PeriodoRecommendation(BaseModel):
    """
    Recomendación generada a partir de un PeriodoReport.
    Almacena el contexto completo para saber bajo qué circunstancias fue emitida.
    """

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="periodo_recommendations",
        on_delete=fields.CASCADE,
    )
    periodo = fields.ForeignKeyField(
        "models.Periodo",
        related_name="recommendations",
        on_delete=fields.CASCADE,
    )
    report = fields.ForeignKeyField(
        "models.PeriodoReport",
        related_name="recommendations",
        on_delete=fields.CASCADE,
    )

    # ── Clasificación ────────────────────────────────────────────
    categoria = fields.CharField(
        max_length=50,
        description="fungicida | monitoreo | riego | general | alerta",
    )
    prioridad = fields.CharField(
        max_length=20,
        description="urgente | alta | media | baja",
    )

    # ── Contenido ────────────────────────────────────────────────
    titulo = fields.CharField(max_length=255)
    contenido = fields.TextField()

    # ── Metadatos ────────────────────────────────────────────────
    etiquetas = fields.JSONField(
        null=True,
        description="Tags como ['late_blight', 'critico', 'preventivo']",
    )

    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "periodo_recommendations"
        ordering = ["-fecha_creacion"]
