from typing import List
from app.schemas.movimiento_schema import MovimientoCreate
from app.schemas.stock_schema import StockResponse, StockUpdate
from app.services import get_MovimientoService
from .BaseService import BaseService
from ..models.stock_model import Stock

class StockService(BaseService):
    def __init__(self, db):
        super().__init__(db, Stock, StockResponse)

    def obtener_alertas(self, tipo: str = None, ubicacion: str = None) -> List[StockResponse]:
        """
            Obtiene los stocks que están por debajo de la cantidad mínima.
            Args:
                tipo (str, optional): Tipo de stock a filtrar ('producto_simple' o 'componente'). Si se proporciona, filtra por ese tipo.
                ubicacion (str, optional): Ubicación del stock a filtrar. Si se proporciona, filtra por esa ubicación.
                articulo_id (str, optional): ID del artículo a filtrar. Si se proporciona, filtra por ese ID.
            Returns:
                List[StockResponse]: Lista de stocks con cantidad por debajo del mínimo.
        """
        query = self.db.query(self.model).filter(self.model.cantidad < self.model.cantidad_minima)

        if tipo:
            query = query.filter(self.model.tipo == tipo)
        if ubicacion:
            query = query.filter(self.model.ubicacion == ubicacion)

        result = query.all()
        return [self.response_schema.model_validate(item, from_attributes=True) for item in result]

    def obtener_por_id_componente(self, id: int) -> StockResponse:
        """
        Obtiene el stock por ID de componente.
        Args:
            id (int): ID del componente.
        Returns:
            StockResponse: Stock asociado al componente.
        Raises:
            ValueError: Si no se encuentra el stock.
        """
        stock = self.db.query(self.model).filter(self.model.id_componente == id).first()
        return stock

    def obtener_por_id_producto_simple(self, id: int) -> StockResponse:
        """
        Obtiene el stock por ID de producto simple.
        Args:
            id (int): ID del producto simple.
        Returns:
            StockResponse: Stock asociado al producto simple.
        Raises:
            ValueError: Si no se encuentra el stock.
        """
        stock = self.db.query(self.model).filter(self.model.id_producto_simple == id).first()
        return stock