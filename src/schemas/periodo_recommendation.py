"""
Schemas para recomendaciones de periodo.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class PeriodoReportCreate(BaseModel):
    """Payload para crear un reporte de periodo con recomendaciones."""
    
    periodo_id: int
    total_predicciones: int
    con_enfermedad: int
    saludables: int
    confianza_promedio: float
    total_detecciones: int
    promedio_detecciones_por_imagen: float
    tasa_consenso: float
    dias_activos: int
    frecuencia_monitoreo: float
    indice_severidad: float
    severidad_maxima: float
    tendencia: str
    enfermedad_predominante: Optional[str] = None
    surcos_monitoreados: Optional[list] = None
    distribucion_enfermedades: Optional[dict] = None
    pico_enfermedad: Optional[dict] = None
    estado_periodo: str = "en_curso"
    etapa_fenologica: Optional[str] = None
    recomendaciones: list["RecomendacionCreate"] = Field(default_factory=list)


class RecomendacionCreate(BaseModel):
    """Recomendación individual para crear."""
    
    categoria: str  # fungicida | nutricion | riego | monitoreo | cosecha | general
    prioridad: str  # urgente | alta | media | baja
    titulo: str
    contenido: str
    aplicable_desde: Optional[date] = None
    aplicable_hasta: Optional[date] = None
    etiquetas: Optional[list[str]] = None


class RecomendacionUpdate(BaseModel):
    """Actualización de estado de una recomendación."""
    
    estado: str  # pendiente | aplicada | descartada | expirada
    notas_usuario: Optional[str] = None


class PeriodoReportRead(BaseModel):
    """Respuesta de un reporte de periodo."""
    
    id: int
    periodo_id: int
    total_predicciones: int
    con_enfermedad: int
    saludables: int
    confianza_promedio: float
    indice_severidad: float
    tendencia: str
    enfermedad_predominante: Optional[str]
    estado_periodo: str
    etapa_fenologica: Optional[str]
    distribucion_enfermedades: Optional[dict]
    fecha_reporte: str
    recomendaciones: Optional[list["RecomendacionRead"]] = None


class RecomendacionRead(BaseModel):
    """Respuesta de una recomendación."""
    
    id: int
    periodo_id: int
    categoria: str
    prioridad: str
    titulo: str
    contenido: str
    estado: str
    aplicable_desde: Optional[str]
    aplicable_hasta: Optional[str]
    etiquetas: Optional[list[str]]
    fecha_creacion: str
    fecha_aplicacion: Optional[str]
    notas_usuario: Optional[str]
