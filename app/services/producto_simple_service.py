from .BaseService import BaseService
from ..models.producto_simple_model import ProductoSimple
from ..schemas.producto_simple_schema import ProductoSimpleResponse, ProductoSimpleCreate, ProductoSimpleUpdate

class ProductoSimpleService(BaseService):
    def __init__(self, db):
        super().__init__(db, ProductoSimple, ProductoSimpleResponse)
