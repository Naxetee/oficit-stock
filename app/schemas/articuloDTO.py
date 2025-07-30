from pydantic import BaseModel, Field, field_validator, validator
from typing import Optional
from decimal import Decimal
from datetime import datetime

class ArticuloBase(BaseModel):
    codigo: str = Field(..., description="Código del artículo")
    nombre: str = Field(..., description="Nombre del artículo")
    descripcion: Optional[str] = Field(None, description="Descripción del artículo")
    precio_compra: Decimal = Field(..., description="Precio de compra")
    precio_venta: Decimal = Field(..., description="Precio de venta")
    stock_minimo: int = Field(0, description="Stock mínimo")
    stock_actual: int = Field(0, description="Stock actual")
    unidad_medida: str = Field(..., description="Unidad de medida")
    familia_id: Optional[int] = Field(None, description="ID de la familia")
    activo: bool = Field(True, description="Estado del artículo")

    @field_validator('precio_compra', 'precio_venta')
    def validate_precios(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloUpdate(BaseModel):
    codigo: Optional[str] = Field(None, description="Código del artículo")
    nombre: Optional[str] = Field(None, description="Nombre del artículo")
    descripcion: Optional[str] = Field(None, description="Descripción del artículo")
    precio_compra: Optional[Decimal] = Field(None, description="Precio de compra")
    precio_venta: Optional[Decimal] = Field(None, description="Precio de venta")
    stock_minimo: Optional[int] = Field(None, description="Stock mínimo")
    stock_actual: Optional[int] = Field(None, description="Stock actual")
    unidad_medida: Optional[str] = Field(None, description="Unidad de medida")
    familia_id: Optional[int] = Field(None, description="ID de la familia")
    activo: Optional[bool] = Field(None, description="Estado del artículo")

class ArticuloInDB(ArticuloBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ArticuloResponse(ArticuloInDB):
    pass
