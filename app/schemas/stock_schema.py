from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StockBase(BaseModel):
    cantidad: int = Field(..., ge=0)
    cantidad_minima: int = Field(..., ge=0)
    ubicacion: Optional[str] = Field(None, max_length=255)
    tipo: str = Field(..., max_length=31, pattern='^(producto_simple|componente)$')
    id_componente: Optional[int] = Field(None, ge=1)
    id_producto_simple: Optional[int] = Field(None, ge=1)
    
class StockCreate(StockBase):
    pass

class StockUpdate(StockBase):
    cantidad: Optional[int] = Field(None, ge=0)
    cantidad_minima: Optional[int] = Field(None, ge=0)
    ubicacion: Optional[str] = Field(None, max_length=255)
    tipo: Optional[str] = Field(None, max_length=31, pattern='^(producto_simple|componente)$')
    id_componente: Optional[int] = Field(None, ge=1)
    id_producto_simple: Optional[int] = Field(None, ge=1)

class StockInDB(StockBase):
    id: int = Field(..., ge=1)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

class StockResponse(StockInDB):
    pass
