from app.schemas.articulo_schema import ArticuloBase, ArticuloCreate, ArticuloInDB, ArticuloUpdate

class ProductoCompuestoBase(ArticuloBase):
    pass

class ProductoCompuestoCreate(ArticuloCreate):
    pass

class ProductoCompuestoUpdate(ArticuloUpdate):
    pass

class ProductoCompuestoInDB(ArticuloInDB):
    pass

class ProductoCompuestoResponse(ProductoCompuestoInDB):
    pass
