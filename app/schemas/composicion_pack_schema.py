from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.articulo_schema import ArticuloResponse

class ComposicionPackResponse(BaseModel):
    articulo: ArticuloResponse
    cantidad: int = Field(..., gt=0, description="Cantidad del producto en el pack")

    class Config:
        from_attributes = True

class ComposicionPackCreate(BaseModel):
    id_pack: int = Field(..., description="ID del pack")
    id_producto: int = Field(..., description="ID del artículo/producto incluido en el pack")
    cantidad: int = Field(..., gt=0, description="Cantidad del producto en el pack")

    class Config:
        from_attributes = True