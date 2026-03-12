from tortoise import fields

from src.models.base import BaseModel


class Modulo(BaseModel):
    nombre = fields.CharField(max_length=255)
    descripcion = fields.TextField(null=True)
    user = fields.ForeignKeyField("models.User", related_name="modulos", on_delete=fields.CASCADE)

    class Meta:
        table = "modulos"
