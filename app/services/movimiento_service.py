from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.movimiento_schema import MovimientoCreate, MovimientoResponse
from app.models.movimiento_model import Movimiento
from app.models.stock_model import Stock
from app.models.producto_simple_model import ProductoSimple
from app.models.componente_model import Componente
from app.schemas.stock_schema import StockResponse
from .BaseService import BaseService

class MovimientoService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Movimiento, MovimientoResponse)

    def _get_or_create_stock_for_producto_simple(self, producto_simple_id: int) -> Stock:
        st = self.db.execute(
            select(Stock).where(
                Stock.tipo == "producto_simple",
                Stock.id_producto_simple == producto_simple_id
            )
        ).scalar_one_or_none()
        if st:
            return st
        st = Stock(
            tipo="producto_simple",
            id_producto_simple=producto_simple_id,
            cantidad=0,
            cantidad_minima=0
        )
        self.db.add(st)
        self.db.flush()
        return st

    def _get_or_create_stock_for_componente(self, componente_id: int) -> Stock:
        st = self.db.execute(
            select(Stock).where(
                Stock.tipo == "componente",
                Stock.id_componente == componente_id
            )
        ).scalar_one_or_none()
        if st:
            return st
        st = Stock(
            tipo="componente",
            id_componente=componente_id,
            cantidad=0,
            cantidad_minima=0
        )
        self.db.add(st)
        self.db.flush()
        return st

    def crear_movimiento(self, data: MovimientoCreate) -> StockResponse:
        # Validación de referencia: exactamente uno de los dos
        if bool(data.id_producto_simple) == bool(data.id_componente):
            raise HTTPException(status_code=422, detail="Indica exactamente uno: id_producto_simple o id_componente")

        try:
            # Validar existencia de entidad destino
            if data.id_producto_simple:
                existe = self.db.get(ProductoSimple, data.id_producto_simple)
                if not existe:
                    raise HTTPException(status_code=404, detail="Producto simple no encontrado")
                stock = self._get_or_create_stock_for_producto_simple(data.id_producto_simple)
            else:
                existe = self.db.get(Componente, data.id_componente)
                if not existe:
                    raise HTTPException(status_code=404, detail="Componente no encontrado")
                stock = self._get_or_create_stock_for_componente(data.id_componente)

            # Calcular nuevo stock
            delta = data.cantidad if data.tipo == "entrada" else -data.cantidad
            nueva_cantidad = (stock.cantidad or 0) + delta
            if nueva_cantidad < 0:
                # No actualizar ni crear movimiento si no hay stock suficiente
                raise HTTPException(status_code=400, detail="No hay stock suficiente para realizar la salida")
            stock.cantidad = nueva_cantidad

            # Crear movimiento
            mov = Movimiento(
                tipo=data.tipo,
                cantidad=data.cantidad,
                id_producto_simple=data.id_producto_simple,
                id_componente=data.id_componente,
                descripcion=data.descripcion,
            )
            self.db.add(mov)

            # Confirmar transacción, refrescar y devolver stock actualizado
            self.db.commit()
            self.db.refresh(stock)
            return stock

        except HTTPException:
            # Re-lanzar errores de negocio/validación
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error al crear movimiento: {str(e)}")