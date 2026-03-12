from tortoise import fields

from src.models.base import BaseModel


# ═══════════════════════════════════════════════════════════════════
#  SURCO
# ═══════════════════════════════════════════════════════════════════

class SurcoReport(BaseModel):
    """
    Snapshot de métricas agregadas de un surco en un momento dado.
    Se genera cuando el usuario solicita el diagnóstico de un surco.
    Almacena todas las métricas que justifican las recomendaciones emitidas.
    """

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="surco_reports",
        on_delete=fields.CASCADE,
    )
    surco = fields.ForeignKeyField(
        "models.Surco",
        related_name="reports",
        on_delete=fields.CASCADE,
    )

    # ── Métricas generales ────────────────────────────────────────
    total_predicciones = fields.IntField()
    con_enfermedad = fields.IntField()
    saludables = fields.IntField()
    confianza_promedio = fields.FloatField()
    total_detecciones = fields.IntField()
    promedio_detecciones_por_imagen = fields.FloatField()
    tasa_consenso = fields.FloatField()

    # ── Severidad e índice ────────────────────────────────────────
    indice_severidad = fields.FloatField(
        description="Porcentaje de predicciones con enfermedad (0-100)"
    )
    tendencia = fields.CharField(
        max_length=30,
        description="mejorando | empeorando | estable | insuficiente_datos",
    )
    enfermedad_predominante = fields.CharField(max_length=100, null=True)

    # ── Distribución detallada ────────────────────────────────────
    distribucion_enfermedades = fields.JSONField(null=True)

    fecha_reporte = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "surco_reports"
        ordering = ["-fecha_reporte"]


class SurcoRecommendation(BaseModel):
    """Recomendación generada a partir de un SurcoReport."""

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="surco_recommendations",
        on_delete=fields.CASCADE,
    )
    surco = fields.ForeignKeyField(
        "models.Surco",
        related_name="recommendations",
        on_delete=fields.CASCADE,
    )
    report = fields.ForeignKeyField(
        "models.SurcoReport",
        related_name="recommendations",
        on_delete=fields.CASCADE,
    )

    categoria = fields.CharField(max_length=50)
    prioridad = fields.CharField(max_length=20)
    titulo = fields.CharField(max_length=255)
    contenido = fields.TextField()
    etiquetas = fields.JSONField(null=True)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "surco_recommendations"
        ordering = ["-fecha_creacion"]


# ═══════════════════════════════════════════════════════════════════
#  LOTE
# ═══════════════════════════════════════════════════════════════════

class LoteReport(BaseModel):
    """
    Snapshot de métricas agregadas de un lote en un momento dado.
    Acumula datos de todos los surcos del lote.
    """

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="lote_reports",
        on_delete=fields.CASCADE,
    )
    lote = fields.ForeignKeyField(
        "models.Lote",
        related_name="reports",
        on_delete=fields.CASCADE,
    )

    # ── Métricas generales ────────────────────────────────────────
    total_predicciones = fields.IntField()
    con_enfermedad = fields.IntField()
    saludables = fields.IntField()
    confianza_promedio = fields.FloatField()
    total_detecciones = fields.IntField()
    promedio_detecciones_por_imagen = fields.FloatField()
    tasa_consenso = fields.FloatField()

    # ── Severidad e índice ────────────────────────────────────────
    indice_severidad = fields.FloatField()
    tendencia = fields.CharField(max_length=30)
    enfermedad_predominante = fields.CharField(max_length=100, null=True)

    # ── Cobertura de surcos ───────────────────────────────────────
    surcos_monitoreados = fields.JSONField(
        null=True,
        description="Lista de IDs de surcos evaluados en el lote",
    )

    # ── Distribución detallada ────────────────────────────────────
    distribucion_enfermedades = fields.JSONField(null=True)

    fecha_reporte = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "lote_reports"
        ordering = ["-fecha_reporte"]


class LoteRecommendation(BaseModel):
    """Recomendación generada a partir de un LoteReport."""

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="lote_recommendations",
        on_delete=fields.CASCADE,
    )
    lote = fields.ForeignKeyField(
        "models.Lote",
        related_name="recommendations",
        on_delete=fields.CASCADE,
    )
    report = fields.ForeignKeyField(
        "models.LoteReport",
        related_name="recommendations",
        on_delete=fields.CASCADE,
    )

    categoria = fields.CharField(max_length=50)
    prioridad = fields.CharField(max_length=20)
    titulo = fields.CharField(max_length=255)
    contenido = fields.TextField()
    etiquetas = fields.JSONField(null=True)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "lote_recommendations"
        ordering = ["-fecha_creacion"]


# ═══════════════════════════════════════════════════════════════════
#  MÓDULO
# ═══════════════════════════════════════════════════════════════════

class ModuloReport(BaseModel):
    """
    Snapshot de métricas agregadas de un módulo en un momento dado.
    Acumula datos de todos los lotes y surcos del módulo.
    """

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="modulo_reports",
        on_delete=fields.CASCADE,
    )
    modulo = fields.ForeignKeyField(
        "models.Modulo",
        related_name="reports",
        on_delete=fields.CASCADE,
    )

    # ── Métricas generales ────────────────────────────────────────
    total_predicciones = fields.IntField()
    con_enfermedad = fields.IntField()
    saludables = fields.IntField()
    confianza_promedio = fields.FloatField()
    total_detecciones = fields.IntField()
    promedio_detecciones_por_imagen = fields.FloatField()
    tasa_consenso = fields.FloatField()

    # ── Severidad e índice ────────────────────────────────────────
    indice_severidad = fields.FloatField()
    tendencia = fields.CharField(max_length=30)
    enfermedad_predominante = fields.CharField(max_length=100, null=True)

    # ── Cobertura espacial ────────────────────────────────────────
    lotes_monitoreados = fields.JSONField(
        null=True,
        description="Lista de IDs de lotes evaluados en el módulo",
    )
    surcos_monitoreados = fields.JSONField(
        null=True,
        description="Lista de IDs de surcos evaluados en el módulo",
    )

    # ── Distribución detallada ────────────────────────────────────
    distribucion_enfermedades = fields.JSONField(null=True)

    fecha_reporte = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "modulo_reports"
        ordering = ["-fecha_reporte"]


class ModuloRecommendation(BaseModel):
    """Recomendación generada a partir de un ModuloReport."""

    usuario = fields.ForeignKeyField(
        "models.User",
        related_name="modulo_recommendations",
        on_delete=fields.CASCADE,
    )
    modulo = fields.ForeignKeyField(
        "models.Modulo",
        related_name="recommendations",
        on_delete=fields.CASCADE,
    )
    report = fields.ForeignKeyField(
        "models.ModuloReport",
        related_name="recommendations",
        on_delete=fields.CASCADE,
    )

    categoria = fields.CharField(max_length=50)
    prioridad = fields.CharField(max_length=20)
    titulo = fields.CharField(max_length=255)
    contenido = fields.TextField()
    etiquetas = fields.JSONField(null=True)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "modulo_recommendations"
        ordering = ["-fecha_creacion"]
