from tortoise import fields
from src.models.base import BaseModel

class User(BaseModel):
  username = fields.CharField(max_length=20, unique=True)
  password = fields.TextField()
  email = fields.CharField(max_length=255, unique=True)
  full_name = fields.CharField(max_length=255, null=True, default=None)
  
  class Meta:
    table = "users"