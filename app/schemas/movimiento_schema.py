from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Integer, func
from sqlalchemy.orm import Mapped, mapped_column



class MovimientoBase(BaseModel):
    """
    Base schema for Movimiento.
    """
    id_producto_simple: Optional[int] = Field(None, description="ID del producto simple.")
    id_componente: Optional[int] = Field(None, description="ID del componente.")
    cantidad: int = Field(..., ge=1, description="Cantidad del movimiento.")
    tipo: str = Field(..., max_length=31, pattern='^(entrada|salida)$', description="Tipo de movimiento: 'entrada' o 'salida'.")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción del movimiento.")

class MovimientoCreate(MovimientoBase):
    """
    Schema for creating a new Movimiento.
    """
    pass

class MovimientoUpdate(MovimientoBase):
    """
    Schema for updating an existing Movimiento.
    """
    id_producto_simple: Optional[int] = Field(None, description="ID del producto simple.")
    id_componente: Optional[int] = Field(None, description="ID del componente.")
    cantidad: Optional[int] = Field(None, ge=1, description="Cantidad del movimiento.")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción del movimiento.")
    tipo: Optional[str] = Field(None, max_length=31, pattern='^(entrada|salida)$', description="Tipo de movimiento: 'entrada' o 'salida'.")

class MovimientoInDB(MovimientoBase):
    """
    Schema for Movimiento stored in the database.
    """
    id: int = Field(..., ge=1, description="ID del movimiento.")
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

class MovimientoResponse(MovimientoInDB):
    """
    Schema for Movimiento response.
    """
    pass