from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class ArticuloBase(BaseModel):
    tipo: Optional[str] = Field(None, pattern="^(simple|compuesto|pack)?$")
    nombre: Optional[str] = Field(None, max_length=255)
    descripcion: Optional[str] = Field(None)
    codigo_tienda: Optional[str] = Field(None, max_length=31)
    id_familia: Optional[int] = Field(None, ge=1)
    activo: Optional[bool] = Field(None)

    @field_validator('tipo')
    def validate_tipo(cls, v):
        if v and v not in ('simple', 'compuesto', 'pack'):
            raise ValueError("Tipo debe ser simple, compuesto o pack")
        return v

    @field_validator('nombre')
    def validate_nombre(cls, v):
        if v and len(v) > 255:
            raise ValueError("El nombre no puede exceder los 255 caracteres")
        if v and not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloUpdate(BaseModel):
    tipo: Optional[str] = Field(None, pattern="^(simple|compuesto|pack)?$")
    nombre: Optional[str] = Field(None, max_length=255)
    descripcion: Optional[str] = Field(None)
    codigo_tienda: Optional[str] = Field(None, max_length=31)
    id_familia: Optional[int] = Field(None, ge=1)
    activo: Optional[bool] = Field(None)

class ArticuloInDB(ArticuloBase):
    id: int = Field(..., ge=1)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

class ArticuloResponse(ArticuloInDB):
    pass