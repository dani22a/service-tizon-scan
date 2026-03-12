from tortoise import fields

from src.models.base import BaseModel


class Prediccion(BaseModel):
    surco = fields.ForeignKeyField("models.Surco", related_name="predicciones", on_delete=fields.CASCADE, null=True)
    usuario = fields.ForeignKeyField("models.User", related_name="predicciones", on_delete=fields.CASCADE, null=True)
    periodo = fields.ForeignKeyField("models.Periodo", related_name="predicciones", on_delete=fields.SET_NULL, null=True)
    imagen_url = fields.TextField(null=True)
    fase1_resumen = fields.JSONField(null=True)
    fase1_payload = fields.JSONField(null=True)
    fase2_resumen = fields.JSONField(null=True)
    fase2_payload = fields.JSONField(null=True)
    fecha = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "predicciones"
