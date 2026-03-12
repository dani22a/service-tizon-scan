from tortoise.models import Model
from tortoise import fields

class BaseModel(Model):
  id = fields.IntField(pk=True, generated=True)
  created_at = fields.DatetimeField(auto_now_add=True, null=True)
  updated_at = fields.DatetimeField(auto_now=True, null=True)
  deleted_at = fields.DatetimeField(null=True)

  class Meta:
    abstract = True