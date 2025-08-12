from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ComponenteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    descripcion: Optional[str] = Field(None)
    id_proveedor: Optional[int] = Field(None, ge=1)
    id_color: Optional[int] = Field(None, ge=1)

class ComponenteCreate(ComponenteBase):
    pass

class ComponenteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    descripcion: Optional[str] = Field(None)
    id_proveedor: Optional[int] = Field(None, ge=1)
    id_color: Optional[int] = Field(None, ge=1)

class ComponenteInDB(ComponenteBase):
    id: int = Field(..., ge=1)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

class ComponenteResponse(ComponenteInDB):
    pass
