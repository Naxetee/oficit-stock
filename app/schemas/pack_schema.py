from app.schemas.articulo_schema import ArticuloBase, ArticuloCreate, ArticuloInDB, ArticuloUpdate

class PackBase(ArticuloBase):
    pass

class PackCreate(ArticuloCreate):
    pass

class PackUpdate(ArticuloUpdate):
    pass

class PackInDB(ArticuloInDB):
    pass

class PackResponse(PackInDB):
    pass
