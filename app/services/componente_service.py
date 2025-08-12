from typing import List
from .BaseService import BaseService
from ..models.componente_model import Componente
from ..models.stock_model import Stock
from ..schemas.componente_schema import ComponenteResponse
from ..models.composicion_prod_compuesto_model import ComposicionProdCompuesto


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

    def agregar_componentes_a_producto_compuesto(self, id_producto_compuesto: int, componentes: List[int]) -> dict:
        """
            Agrega componentes a un producto compuesto.
            Args:
                id_producto_compuesto (int): ID del producto compuesto.
                componentes (List[int]): Lista de IDs de componentes a agregar.
            Returns:
                dict: Mensaje de éxito.
        """

        for componente_id in componentes:
            nueva_composicion = ComposicionProdCompuesto(
                id_producto_compuesto=id_producto_compuesto,
                id_componente=componente_id
            )
            self.db.add(nueva_composicion)
        self.db.commit()
        return {"detail": f"Componentes [{', '.join([comp_id for comp_id in componentes])}] agregados al producto compuesto exitosamente."}