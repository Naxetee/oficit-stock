from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ColorBase(BaseModel):
    nombre: str = Field(..., description="Nombre del color")
    codigo_hex: Optional[str] = Field(None, description="Código hexadecimal del color")
    descripcion: Optional[str] = Field(None, description="Descripción del color")
    id_familia: Optional[int] = Field(None, description="ID de la familia asociada")
    activo: bool = Field(True, description="Estado del color")

class ColorCreate(ColorBase):
    pass

class ColorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, description="Nombre del color")
    codigo_hex: Optional[str] = Field(None, description="Código hexadecimal del color")
    descripcion: Optional[str] = Field(None, description="Descripción del color")
    id_familia: Optional[int] = Field(None, description="ID de la familia asociada")
    activo: Optional[bool] = Field(None, description="Estado del color")

class ColorInDB(ColorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ColorResponse(ColorInDB):
    pass
