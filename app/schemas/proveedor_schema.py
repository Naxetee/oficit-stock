from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ProveedorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=127)
    telefono: Optional[str] = Field(None, max_length=31)
    email: Optional[str] = Field(None, max_length=127)
    direccion: Optional[str] = Field(None, max_length=255)
    activo: Optional[bool] = Field(None)

    @field_validator('nombre')
    def validate_nombre(cls, v):
        if not v or not v.strip():
            raise ValueError("El nombre del proveedor no puede estar vacío")
        return v

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=127)
    telefono: Optional[str] = Field(None, max_length=31)
    email: Optional[str] = Field(None, max_length=127)
    direccion: Optional[str] = Field(None, max_length=255)
    activo: Optional[bool] = Field(None)

class ProveedorInDB(ProveedorBase):
    id: int = Field(..., ge=1)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

class ProveedorResponse(ProveedorInDB):
    pass
