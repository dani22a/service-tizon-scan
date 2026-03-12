from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ModuloCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    descripcion: str | None = None


class LoteCreate(BaseModel):
    identificador: str = Field(..., min_length=1, max_length=100)
    descripcion: str | None = None


class SurcoCreate(BaseModel):
    numero: int = Field(..., ge=1)
    descripcion: str | None = None


class ModuloResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    created_at: str | None
    updated_at: str | None


class LoteResponse(BaseModel):
    id: int
    modulo_id: int
    identificador: str
    descripcion: str | None
    created_at: str | None
    updated_at: str | None


class SurcoResponse(BaseModel):
    id: int
    lote_id: int
    numero: int
    descripcion: str | None
    created_at: str | None
    updated_at: str | None


class PrediccionResponse(BaseModel):
    id: int
    surco_id: int
    usuario_id: int
    imagen_url: str
    fase1_resumen: dict[str, Any]
    fase1_payload: dict[str, Any]
    fase2_resumen: dict[str, Any]
    fase2_payload: dict[str, Any]
    fecha: str
    created_at: str | None
    updated_at: str | None
