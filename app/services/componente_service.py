from typing import List, Optional, Tuple

from app.schemas.composicion_producto_compuesto_schema import ComposicionProdCompuestoCreate
from app.services import get_ProductoCompuestoService
from .BaseService import BaseService
from ..models.componente_model import Componente
from ..models.stock_model import Stock
from ..schemas.componente_schema import ComponenteResponse
from ..models.composicion_prod_compuesto_model import ComposicionProdCompuesto
from fastapi import HTTPException

class ComponenteService(BaseService):
    def __init__(self, db):
        super().__init__(db, Componente, ComponenteResponse)

    def obtener_componentes_por_producto_compuesto(self, id_producto_compuesto: int) -> Optional[List[ComponenteResponse]]:
        """
            Obtiene los componentes asociados a un producto compuesto.
            Args:
                id_producto_compuesto (int): ID del producto compuesto.
            Returns:
                List[ComponenteResponse]: Lista de componentes asociados al producto compuesto.
        """
        prod_service = get_ProductoCompuestoService()(self.db)
        if prod_service.obtener_por_id(id_producto_compuesto) is None:
            raise HTTPException(status_code=404, detail=f"Producto compuesto con ID {id_producto_compuesto} no encontrado.")
        query = self.db.query(self.model).join(
            ComposicionProdCompuesto,
            Componente.id == ComposicionProdCompuesto.id_componente
        ).filter(
            ComposicionProdCompuesto.id_producto_compuesto == id_producto_compuesto
        )

        componentes = query.all()
        return componentes if componentes else []

    def agregar_componentes_a_producto_compuesto(self, id_producto_compuesto: int, componentes: List[ComposicionProdCompuestoCreate]) -> dict:
        """
            Agrega componentes a un producto compuesto.
            Args:
                id_producto_compuesto (int): ID del producto compuesto.
                componentes (List[ComposicionProdCompuestoCreate]): Lista de ComposicionProdCompuestoCreate que contienen los IDs de los componentes y sus cantidades.
            Returns:
                dict: Mensaje de éxito.
        """
        prod_service = get_ProductoCompuestoService()(self.db)
        if prod_service.obtener_por_id(id_producto_compuesto) is None:
            raise HTTPException(status_code=404, detail=f"Producto compuesto con ID {id_producto_compuesto} no encontrado.")
        
        componentes_existentes = [x.id for x in self.obtener_componentes_por_producto_compuesto(id_producto_compuesto)]
        if any(componente.id_componente in componentes_existentes for componente in componentes):
            raise HTTPException(status_code=400, detail="Uno o más componentes ya están asociados al producto compuesto.")
        for c in componentes:
            nueva_composicion = ComposicionProdCompuesto(
                id_producto_compuesto=id_producto_compuesto,
                id_componente= c.id_componente,
                cantidad=c.cantidad
            )
            self.db.add(nueva_composicion)
        self.db.commit()
        return {"detail": f"Componentes [{', '.join([str(comp_id) for comp_id in componentes])}] agregados al producto compuesto exitosamente."}

    def eliminar_componentes_de_producto_compuesto(self, id: int, componentes: List[int]) -> dict:
        """
            Elimina componentes de un producto compuesto.
            Args:
                id (int): ID del producto compuesto.
                componentes (List[int]): Lista de IDs de componentes a eliminar.
            Returns:
                dict: Mensaje de éxito.
        """
        componentes_existentes = self.obtener_componentes_por_producto_compuesto(id)
        existentes_ids = {componente.id for componente in componentes_existentes}
        # Si alguno de los componentes a eliminar no está asociado, error
        if not set(componentes).issubset(existentes_ids):
            raise HTTPException(status_code=400, detail="Uno o más componentes no están asociados al producto compuesto.")
        for componente_id in componentes:
            self.db.query(ComposicionProdCompuesto).filter(
                ComposicionProdCompuesto.id_producto_compuesto == id,
                ComposicionProdCompuesto.id_componente == componente_id
            ).delete()
        self.db.commit()
        return {"detail": f"Componentes [{', '.join(map(str, componentes))}] eliminados del producto compuesto exitosamente."}