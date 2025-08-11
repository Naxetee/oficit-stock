from typing import List
from .BaseService import BaseService
from ..models.componente_model import Componente
from ..models.stock_model import Stock
from ..schemas.componente_schema import ComponenteResponse

class ComponenteService(BaseService):
    def __init__(self, db):
        super().__init__(db, Componente, ComponenteResponse)

    def obtener_stock(self, id: int = None) -> List[ComponenteResponse]:
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

    def obtener_componentes_por_producto_compuesto(self, id_producto_compuesto: int) -> List[ComponenteResponse]:
        """
            Obtiene los componentes asociados a un producto compuesto.
            Args:
                id_producto_compuesto (int): ID del producto compuesto.
            Returns:
                List[ComponenteResponse]: Lista de componentes asociados al producto compuesto.
        """
        from ..models.composicion_prod_compuesto_model import ComposicionProdCompuesto
        from sqlalchemy.orm import joinedload

        query = self.db.query(Componente).join(
            ComposicionProdCompuesto,
            Componente.id == ComposicionProdCompuesto.id_componente
        ).filter(
            ComposicionProdCompuesto.id_producto_compuesto == id_producto_compuesto
        ).options(joinedload(Componente.Composicion_Prod_Compuesto))

        return query.all()