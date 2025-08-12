from typing import List, Optional
from sqlalchemy.orm import Session
from .BaseService import BaseService
from ..models.stock_model import Stock
from app.schemas.stock_schema import StockResponse

class StockService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Stock, StockResponse)

    def obtener_alertas(self, tipo: Optional[str] = None, ubicacion: Optional[str] = None) -> List[StockResponse]:
        query = self.db.query(self.model).filter(self.model.cantidad < self.model.cantidad_minima)
        if tipo:
            query = query.filter(self.model.tipo == tipo)
        if ubicacion:
            query = query.filter(self.model.ubicacion == ubicacion)
        result = query.all()
        return [self.response_schema.model_validate(item, from_attributes=True) for item in result]

    def obtener_por_id_componente(self, id: int):
        return self.db.query(self.model).filter(self.model.id_componente == id).first()

    def obtener_por_id_producto_simple(self, id: int):
        return self.db.query(self.model).filter(self.model.id_producto_simple == id).first()