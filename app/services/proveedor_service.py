from .BaseService import BaseService
from ..models.proveedor_model import Proveedor
from ..schemas.proveedor_schema import ProveedorResponse, ProveedorCreate, ProveedorUpdate

class ProveedorService(BaseService):
    def __init__(self, db):
        super().__init__(db, Proveedor, ProveedorResponse)
