from ast import List
from app.schemas.stock_schema import StockResponse
from .BaseService import BaseService
from ..models.componente_model import Componente
from ..models.stock_model import Stock
from ..schemas.componente_schema import ComponenteResponse

class ComponenteService(BaseService):
    def __init__(self, db):
        super().__init__(db, Componente, ComponenteResponse)

    def obtener_stock(self, id: int = None) -> List[StockResponse]:
        """
            Obtiene los stocks de todos los componentes.
            Args:
                id (int, optional): ID del componente específico. Si se proporciona, filtra por ese ID.
            Returns:
                List[StockResponse]: Lista de stocks de componentes.
        """
        if id:
            stocks = self.db.query(Stock).filter(Stock.tipo == 'componente', Stock.id_componente == id)
        else:
            stocks = self.db.query(Stock).filter(Stock.tipo == 'componente')
        return stocks.all()