from .BaseService import BaseService
from ..models.pack_model import Pack
from ..schemas.pack_schema import PackResponse, PackCreate, PackUpdate

class PackService(BaseService):
    def __init__(self, db):
        super().__init__(db, Pack, PackResponse)
