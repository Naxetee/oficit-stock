from fastapi import HTTPException
from app.schemas.movimiento_schema import MovimientoCreate, MovimientoResponse
from app.models.movimiento_model import Movimiento
from app.schemas.stock_schema import StockResponse
from app.services import get_StockService
from .BaseService import BaseService

class MovimientoService(BaseService):
    def __init__(self, db):
        super().__init__(db, Movimiento, MovimientoResponse)

    def crear_movimiento(self, data: MovimientoCreate) -> StockResponse:
        """
        Crea un nuevo movimiento de stock.
        Args:
            data (MovimientoCreate): Datos del movimiento a crear.
        Returns:
            StockResponse: Stock actualizado después del movimiento.
        """
        try:
            self.crear(data)
            stock_service = get_StockService()(self.db)
            stock = stock_service.obtener_por_id_componente(data.id_componente) if data.id_componente else \
                    stock_service.obtener_por_id_producto_simple(data.id_producto_simple)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error al crear movimiento: {str(e)}")
        return stock
        