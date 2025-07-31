from pydantic import BaseModel, Field, field_validator, validator
from typing import Optional
from decimal import Decimal
from datetime import datetime

class ArticuloBase(BaseModel):
    codigo: str = Field(..., description="Código del artículo")
    nombre: str = Field(..., description="Nombre del artículo")
    descripcion: Optional[str] = Field(None, description="Descripción del artículo")
    id_familia: Optional[int] = Field(None, description="ID de la familia")
    activo: bool = Field(True, description="Estado del artículo")
    @field_validator('nombre')
    def validar_nombre(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloUpdate(BaseModel):
    codigo: Optional[str] = Field(None, description="Código del artículo")
    nombre: Optional[str] = Field(None, description="Nombre del artículo")
    descripcion: Optional[str] = Field(None, description="Descripción del artículo")
    id_familia: Optional[int] = Field(None, description="ID de la familia")
    activo: Optional[bool] = Field(None, description="Estado del artículo")
    @field_validator('nombre')
    def validar_nombre(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

class ArticuloInDB(ArticuloBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ArticuloResponse(ArticuloInDB):
    pass
