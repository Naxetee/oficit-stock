from .BaseService import BaseService
from ..models.producto_compuesto_model import ProductoCompuesto
from ..schemas.producto_compuesto_schema import ProductoCompuestoResponse, ProductoCompuestoCreate, ProductoCompuestoUpdate

class ProductoCompuestoService(BaseService):
    def __init__(self, db):
        super().__init__(db, ProductoCompuesto, ProductoCompuestoResponse)
