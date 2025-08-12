from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ColorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=31)
    hex: Optional[str] = Field(None, max_length=7)
    url_imagen: Optional[str] = Field(None, max_length=511)
    id_familia: Optional[int] = Field(None, ge=1)

class ColorCreate(ColorBase):
    pass

class ColorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=31)
    hex: Optional[str] = Field(None, max_length=7)
    url_imagen: Optional[str] = Field(None, max_length=511)
    id_familia: Optional[int] = Field(None, ge=1)

class ColorInDB(ColorBase):
    id: int = Field(..., ge=1)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

class ColorResponse(ColorInDB):
    pass
