from pydantic import BaseModel, Field
from datetime import date


class PeriodoCreate(BaseModel):
    nombre: str = Field(..., max_length=255)
    descripcion: str | None = None
    fecha_inicio: date
    fecha_fin: date


class PeriodoRead(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    fecha_inicio: date
    fecha_fin: date
    usuario_id: int
    created_at: date | None
    updated_at: date | None


class PeriodoUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
