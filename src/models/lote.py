from tortoise import fields

from src.models.base import BaseModel


class Lote(BaseModel):
    identificador = fields.CharField(max_length=100)
    descripcion = fields.TextField(null=True)
    modulo = fields.ForeignKeyField("models.Modulo", related_name="lotes", on_delete=fields.CASCADE)

    class Meta:
        table = "lotes"
        unique_together = (("modulo_id", "identificador"),)
