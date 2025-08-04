from .BaseService import BaseService
from ..models.color_model import Color
from ..schemas.color_schema import ColorResponse, ColorCreate, ColorUpdate

class ColorService(BaseService):
    def __init__(self, db):
        super().__init__(db, Color, ColorResponse)
