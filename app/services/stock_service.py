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
            
    def obtener_resumen_inventario(self) -> Dict[str, Any]:
        """Obtener resumen general del inventario"""
        try:
            todos_stocks = self.obtener_todos()
            stocks_bajo_minimo = self.obtener_stock_bajo_minimo()
            
            valor_total_aproximado = 0
            productos_con_stock = 0
            componentes_con_stock = 0
            
            for stock in todos_stocks:
                if stock.cantidad_actual > 0:
                    if stock.id_producto_simple:
                        productos_con_stock += 1
                        # Calcular valor aproximado si tiene precio
                        producto = self.db.query(ProductoSimple).filter(
                            ProductoSimple.id == stock.id_producto_simple
                        ).first()
                        if producto and producto.precio_compra:
                            valor_total_aproximado += float(stock.cantidad_actual * producto.precio_compra.valor)
                    else:
                        componentes_con_stock += 1
                        # Calcular valor aproximado de componentes
                        componente = self.db.query(Componente).filter(
                            Componente.id == stock.id_componente
                        ).first()
                        if componente and componente.precio_compra:
                            valor_total_aproximado += float(stock.cantidad_actual * componente.precio_compra.valor)
                            
            return {
                'total_elementos_inventario': len(todos_stocks),
                'productos_con_stock': productos_con_stock,
                'componentes_con_stock': componentes_con_stock,
                'elementos_bajo_minimo': len(stocks_bajo_minimo),
                'valor_aproximado_inventario': valor_total_aproximado,
                'alertas_reposicion': len(stocks_bajo_minimo) > 0
            }
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo resumen de inventario: {e}")
            raise
