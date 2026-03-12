from tortoise import fields

from src.models.base import BaseModel


class Surco(BaseModel):
    numero = fields.IntField()
    descripcion = fields.TextField(null=True)
    lote = fields.ForeignKeyField("models.Lote", related_name="surcos", on_delete=fields.CASCADE)

    class Meta:
        table = "surcos"
        unique_together = (("lote_id", "numero"),)
