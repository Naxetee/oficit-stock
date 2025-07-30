# app/schemas/familiaDTO.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class FamiliaBase(BaseModel):
    nombre: str = Field(..., description="Nombre de la familia (único en el sistema)")
    descripcion: Optional[str] = Field(None, description="Descripción detallada de la familia")

class FamiliaCreate(FamiliaBase):
    @field_validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v
    pass

class FamiliaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, description="Nombre de la familia (único en el sistema)")
    descripcion: Optional[str] = Field(None, description="Descripción detallada de la familia")
    @field_validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v

class FamiliaInDB(FamiliaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class FamiliaResponse(FamiliaInDB):
    pass
