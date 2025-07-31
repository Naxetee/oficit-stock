from pydantic import BaseModel, Field
from typing import Optional, Literal
from decimal import Decimal
from datetime import datetime

class MovimientoInventarioBase(BaseModel):
    articulo_id: int = Field(..., description="ID del artículo")
    tipo_movimiento: Literal["entrada", "salida"] = Field(..., description="Tipo de movimiento")
    cantidad: int = Field(..., description="Cantidad del movimiento")
    motivo: str = Field(..., description="Motivo del movimiento")
    referencia: Optional[str] = Field(None, description="Referencia del documento")
    observaciones: Optional[str] = Field(None, description="Observaciones")

class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass

class MovimientoInventarioUpdate(BaseModel):
    motivo: Optional[str] = Field(None, description="Motivo del movimiento")
    referencia: Optional[str] = Field(None, description="Referencia del documento")
    observaciones: Optional[str] = Field(None, description="Observaciones")

class MovimientoInventarioInDB(MovimientoInventarioBase):
    id: int
    fecha_movimiento: datetime
    usuario_id: Optional[int]
    stock_anterior: int
    stock_nuevo: int
    created_at: datetime
    updated_at: Optional[datetime]

class MovimientoInventarioResponse(MovimientoInventarioInDB):
    pass

class InventarioResumen(BaseModel):
    total_articulos: int
    articulos_bajo_minimo: int
    valor_total_inventario: Decimal
    movimientos_mes: int
