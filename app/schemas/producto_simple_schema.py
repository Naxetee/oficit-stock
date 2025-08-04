from pydantic import Field
from typing import Optional

from app.schemas.articulo_schema import ArticuloBase, ArticuloCreate, ArticuloInDB, ArticuloUpdate

class ProductoSimpleBase(ArticuloBase):
    id_proveedor: Optional[int] = Field(None, ge=1)
    id_color: Optional[int] = Field(None, ge=1)

class ProductoSimpleCreate(ArticuloCreate):
    pass

class ProductoSimpleUpdate(ArticuloUpdate):
    id_proveedor: Optional[int] = Field(None, ge=1)
    id_color: Optional[int] = Field(None, ge=1)

class ProductoSimpleInDB(ArticuloInDB):
    pass

class ProductoSimpleResponse(ProductoSimpleInDB):
    pass
