from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ProductoCompuestoBase(BaseModel):
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

class ProductoCompuestoCreate(ProductoCompuestoBase):
    pass

class ProductoCompuestoUpdate(BaseModel):
    tipo: Optional[str] = Field(None, pattern="^(simple|compuesto|pack)?$")
    nombre: Optional[str] = Field(None, max_length=255)
    descripcion: Optional[str] = Field(None)
    codigo_tienda: Optional[str] = Field(None, max_length=31)
    id_familia: Optional[int] = Field(None, ge=1)
    activo: Optional[bool] = Field(None)

class ProductoCompuestoInDB(ProductoCompuestoBase):
    id: int = Field(..., ge=1)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

class ProductoCompuestoResponse(ProductoCompuestoInDB):
    pass
