from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class FamiliaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=127)
    descripcion: Optional[str] = Field(None, max_length=255)

    @field_validator('nombre')
    def validate_nombre(cls, v):
        if not v or not v.strip():
            raise ValueError("El nombre de la familia no puede estar vacío")
        return v

class FamiliaCreate(FamiliaBase):
    pass

class FamiliaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=127)
    descripcion: Optional[str] = Field(None, max_length=255)

class FamiliaInDB(FamiliaBase):
    id: int = Field(..., ge=1)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

class FamiliaResponse(FamiliaInDB):
    pass
