from .BaseService import BaseService
from ..models.componente_model import Componente
from ..schemas.componente_schema import ComponenteResponse, ComponenteCreate, ComponenteUpdate

class ComponenteService(BaseService):
    def __init__(self, db):
        super().__init__(db, Componente, ComponenteResponse)
