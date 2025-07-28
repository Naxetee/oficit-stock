"""
📦 Servicio de Pack - Gestión de packs de productos
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal

from app.models.pack import Pack
from app.models.pack_producto import PackProducto
from app.models.articulo import Articulo
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class PackService(BaseService):
    """📦 Servicio para gestión de packs"""
    
    def __init__(self, db_session: Session):
        super().__init__(db_session, Pack)
        
    def crear_pack_completo(self, nombre: str, id_articulo: int, 
                          descripcion: str = None, descuento_porcentaje: int = 0,
                          productos_incluidos: List[Dict] = None) -> Dict[str, Any]:
        """
        Crear pack completo con productos incluidos
        
        Args:
            productos_incluidos: Lista de dicts con 'id_producto' y 'cantidad_incluida'
        """
        try:
            # Crear pack
            pack = self.crear(
                nombre=nombre,
                id_articulo=id_articulo,
                descripcion=descripcion,
                descuento_porcentaje=descuento_porcentaje
            )
            
            # Agregar productos al pack
            pack_productos = []
            if productos_incluidos:
                for producto_info in productos_incluidos:
                    pack_producto = PackProducto(
                        id_pack=pack.id,
                        id_producto=producto_info['id_producto'],
                        cantidad_incluida=Decimal(producto_info.get('cantidad_incluida', 1))
                    )
                    self.db.add(pack_producto)
                    pack_productos.append(pack_producto)
                    
                self.db.commit()
                for pp in pack_productos:
                    self.db.refresh(pp)
            
            logger.info(f"✅ Pack '{nombre}' creado con {len(pack_productos)} productos")
            return {'pack': pack, 'pack_productos': pack_productos}
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error creando pack completo: {e}")
            raise
            
    def agregar_producto_a_pack(self, pack_id: int, producto_id: int, 
                              cantidad_incluida: float = 1) -> PackProducto:
        """Agregar un producto a un pack existente"""
        try:
            pack_producto = PackProducto(
                id_pack=pack_id,
                id_producto=producto_id,
                cantidad_incluida=Decimal(cantidad_incluida)
            )
            
            self.db.add(pack_producto)
            self.db.commit()
            self.db.refresh(pack_producto)
            
            return pack_producto
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error agregando producto a pack: {e}")
            raise
            
    def obtener_productos_del_pack(self, pack_id: int) -> List[PackProducto]:
        """Obtener todos los productos incluidos en un pack"""
        return self.db.query(PackProducto).filter(PackProducto.id_pack == pack_id).all()
        
    def calcular_precio_pack(self, pack_id: int) -> Dict[str, Any]:
        """Calcular el precio total del pack con descuento"""
        pack = self.obtener_por_id(pack_id)
        if not pack:
            return {'error': 'Pack no encontrado'}
            
        productos_pack = self.obtener_productos_del_pack(pack_id)
        precio_total = Decimal('0')
        detalles = []
        
        for pp in productos_pack:
            if pp.producto.articulo.precio_venta:
                precio_unitario = pp.producto.articulo.precio_venta.valor
                precio_linea = precio_unitario * pp.cantidad_incluida
                precio_total += precio_linea
                
                detalles.append({
                    'producto_id': pp.id_producto,
                    'nombre': pp.producto.articulo.nombre,
                    'cantidad': float(pp.cantidad_incluida),
                    'precio_unitario': float(precio_unitario),
                    'precio_linea': float(precio_linea)
                })
                
        # Aplicar descuento
        descuento = (precio_total * pack.descuento_porcentaje) / 100
        precio_final = precio_total - descuento
        
        return {
            'precio_sin_descuento': float(precio_total),
            'descuento_porcentaje': pack.descuento_porcentaje,
            'descuento_cantidad': float(descuento),
            'precio_final': float(precio_final),
            'productos': detalles
        }
