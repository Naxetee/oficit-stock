from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ColorBase(BaseModel):
    nombre: str = Field(..., description="Nombre del color")
    codigo_hex: Optional[str] = Field(None, description="Código hexadecimal del color")
    descripcion: Optional[str] = Field(None, description="Descripción del color")
    id_familia: Optional[int] = Field(None, description="ID de la familia asociada")
    activo: bool = Field(True, description="Estado del color")
    url_imagen: Optional[str] = Field(None, description="URL de imagen representativa del color")

class ColorCreate(ColorBase):
    @field_validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v
    @field_validator('codigo_hex')
    def codigo_hex_valido(cls, v):
        if v and not v.startswith('#'):
            raise ValueError('El código hexadecimal debe comenzar con #')
        if v and (len(v) > 7 or any(c not in '0123456789abcdefABCDEF' for c in v[1:])):
            raise ValueError('El código hexadecimal debe ser válido')
        return v
    pass

class ColorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, description="Nombre del color")
    codigo_hex: Optional[str] = Field(None, description="Código hexadecimal del color")
    descripcion: Optional[str] = Field(None, description="Descripción del color")
    id_familia: Optional[int] = Field(None, description="ID de la familia asociada")
    activo: Optional[bool] = Field(None, description="Estado del color")
    url_imagen: Optional[str] = Field(None, description="URL de imagen representativa del color")
    @field_validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v
    pass
class ColorInDB(ColorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ColorResponse(ColorInDB):
    pass
