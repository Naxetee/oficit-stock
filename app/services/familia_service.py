from .BaseService import BaseService
from ..models.familia_model import Familia
from ..schemas.familia_schema import FamiliaResponse, FamiliaCreate, FamiliaUpdate

class FamiliaService(BaseService):
    def __init__(self, db):
        super().__init__(db, Familia, FamiliaResponse)
