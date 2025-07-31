"""
🏬 Servicio de Stock - Gestión de inventario y stock
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal

from app.models.stock import Stock
from app.models.producto_simple import ProductoSimple
from app.models.componente import Componente
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class StockService(BaseService):
    """🏬 Servicio para gestión de stock e inventario"""
    
    def __init__(self, db_session: Session):
        super().__init__(db_session, Stock)
        
    def actualizar_stock(self, stock_id: int, nueva_cantidad: float, 
                        motivo: str = None) -> Optional[Stock]:
        """Actualizar cantidad de stock con log del motivo"""
        try:
            stock = self.obtener_por_id(stock_id)
            if not stock:
                return None
                
            cantidad_anterior = stock.cantidad_actual
            stock.cantidad_actual = Decimal(nueva_cantidad)
            
            self.db.commit()
            self.db.refresh(stock)
            
            logger.info(f"✅ Stock {stock_id} actualizado: {cantidad_anterior} → {nueva_cantidad}. Motivo: {motivo}")
            return stock
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error actualizando stock {stock_id}: {e}")
            raise
            
    def obtener_stock_bajo_minimo(self) -> List[Stock]:
        """Obtener todos los stocks que están por debajo del mínimo"""
        return self.db.query(Stock).filter(
            Stock.cantidad_actual < Stock.cantidad_minima
        ).all()
        
    def obtener_stock_por_producto(self, producto_id: int) -> Optional[Stock]:
        """Obtener stock de un producto simple"""
        return self.db.query(Stock).filter(Stock.id_producto_simple == producto_id).first()
        
    def obtener_stock_por_componente(self, componente_id: int) -> Optional[Stock]:
        """Obtener stock de un componente"""
        return self.db.query(Stock).filter(Stock.id_componente == componente_id).first()
        
    def crear_movimiento_stock(self, stock_id: int, tipo_movimiento: str,
                             cantidad: float, motivo: str = None) -> Dict[str, Any]:
        """
        Crear un movimiento de stock (entrada/salida)
        
        Args:
            tipo_movimiento: 'entrada' o 'salida'
        """
        try:
            stock = self.obtener_por_id(stock_id)
            if not stock:
                return {'error': 'Stock no encontrado'}
                
            cantidad_anterior = float(stock.cantidad_actual)
            
            if tipo_movimiento == 'entrada':
                nueva_cantidad = stock.cantidad_actual + Decimal(cantidad)
            elif tipo_movimiento == 'salida':
                if stock.cantidad_actual < Decimal(cantidad):
                    return {'error': 'No hay suficiente stock disponible'}
                nueva_cantidad = stock.cantidad_actual - Decimal(cantidad)
            else:
                return {'error': 'Tipo de movimiento inválido'}
                
            stock.cantidad_actual = nueva_cantidad
            self.db.commit()
            self.db.refresh(stock)
            
            return {
                'movimiento_exitoso': True,
                'tipo_movimiento': tipo_movimiento,
                'cantidad_movida': cantidad,
                'cantidad_anterior': cantidad_anterior,
                'cantidad_nueva': float(nueva_cantidad),
                'motivo': motivo
            }
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error en movimiento de stock: {e}")
            raise