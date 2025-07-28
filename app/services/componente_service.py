"""
🔩 Servicio de Componente - Gestión de componentes para productos compuestos
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.componente import Componente
from app.models.componente_producto import ComponenteProducto
from app.models.stock import Stock
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class ComponenteService(BaseService):
    """🔩 Servicio para gestión de componentes"""
    
    def __init__(self, db_session: Session):
        super().__init__(db_session, Componente)
        
    def crear_componente_completo(self, nombre: str, descripcion: str = None,
                                codigo: str = None, especificaciones: str = None,
                                unidad_medida: str = 'unidad', id_proveedor: int = None,
                                id_precio_compra: int = None, id_color: int = None,
                                stock_inicial: float = 0, stock_minimo: float = 0,
                                ubicacion_almacen: str = None) -> Dict[str, Any]:
        """Crear componente completo con stock inicial"""
        try:
            # Crear componente
            componente = self.crear(
                nombre=nombre,
                descripcion=descripcion,
                codigo=codigo,
                especificaciones=especificaciones,
                unidad_medida=unidad_medida,
                id_proveedor=id_proveedor,
                id_precio_compra=id_precio_compra,
                id_color=id_color
            )
            
            # Crear stock inicial
            stock = Stock(
                cantidad_actual=stock_inicial,
                cantidad_minima=stock_minimo,
                ubicacion_almacen=ubicacion_almacen,
                id_componente=componente.id
            )
            
            self.db.add(stock)
            self.db.commit()
            self.db.refresh(stock)
            
            logger.info(f"✅ Componente '{nombre}' creado con stock inicial")
            return {'componente': componente, 'stock': stock}
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error creando componente completo: {e}")
            raise
            
    def obtener_por_codigo(self, codigo: str) -> Optional[Componente]:
        """Obtener componente por código"""
        return self.db.query(Componente).filter(Componente.codigo == codigo).first()
        
    def obtener_productos_que_usan_componente(self, componente_id: int) -> List[ComponenteProducto]:
        """Obtener productos compuestos que usan este componente"""
        return self.db.query(ComponenteProducto).filter(
            ComponenteProducto.id_componente == componente_id
        ).all()
        
    def obtener_stock_componente(self, componente_id: int) -> Optional[Stock]:
        """Obtener stock de un componente"""
        return self.db.query(Stock).filter(Stock.id_componente == componente_id).first()
        
    def validar_eliminacion(self, componente_id: int) -> Dict[str, Any]:
        """Validar si un componente puede ser eliminado"""
        productos_usando = self.obtener_productos_que_usan_componente(componente_id)
        stock = self.obtener_stock_componente(componente_id)
        
        puede_eliminar = len(productos_usando) == 0 and (not stock or stock.cantidad_actual == 0)
        
        return {
            'puede_eliminar': puede_eliminar,
            'productos_usando': len(productos_usando),
            'stock_actual': float(stock.cantidad_actual) if stock else 0,
            'razon': 'El componente está siendo usado por productos' if productos_usando else None
        }
