from ast import List
from app.schemas.stock_schema import StockResponse
from .BaseService import BaseService
from ..models.stock_model import Stock

class StockService(BaseService):
    def __init__(self, db):
        super().__init__(db, Stock, StockResponse)

    def obtener_alertas(self, tipo: str = None) -> List[StockResponse]:
        """
            Obtiene los stocks que están por debajo de la cantidad mínima.
            Args:
                tipo (str, optional): Tipo de stock a filtrar ('producto_simple' o 'componente'). Si se proporciona, filtra por ese tipo.
            Returns:
                List[StockResponse]: Lista de stocks con cantidad por debajo del mínimo.
        """
        if tipo:
            stocks = self.db.query(Stock).filter(
                Stock.tipo == tipo,
                Stock.cantidad < Stock.cantidad_minima
            )
        else:
            stocks = self.db.query(Stock).filter(
                Stock.cantidad < Stock.cantidad_minima
            )
        return stocks.all()