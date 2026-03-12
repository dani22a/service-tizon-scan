from tortoise import fields

from src.models.base import BaseModel


class Periodo(BaseModel):
    nombre = fields.CharField(max_length=255)
    descripcion = fields.TextField(null=True)
    fecha_inicio = fields.DateField()
    fecha_fin = fields.DateField()
    usuario = fields.ForeignKeyField("models.User", related_name="periodos", on_delete=fields.CASCADE)

    class Meta:
        table = "periodos"
        # Could add unique_together if needed (eg nombre por usuario)
