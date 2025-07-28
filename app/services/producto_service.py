"""
📦 Servicio de Producto - Gestión de productos simples y compuestos

Este servicio maneja todas las operaciones relacionadas con los productos,
incluyendo la gestión polimórfica de productos simples y compuestos.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal

from app.models.producto import Producto
from app.models.producto_simple import ProductoSimple
from app.models.producto_compuesto import ProductoCompuesto
from app.models.articulo import Articulo
from app.models.componente_producto import ComponenteProducto
from app.models.stock import Stock
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class ProductoService(BaseService):
    """
    📦 Servicio para gestión de productos
    
    Maneja operaciones específicas de productos incluyendo:
    - CRUD de productos simples y compuestos  
    - Gestión polimórfica según tipo
    - Cálculo de costos de productos compuestos
    - Validaciones de componentes requeridos
    """
    
    def __init__(self, db_session: Session):
        super().__init__(db_session, Producto)
        
    def crear_producto_simple_completo(self, id_articulo: int, especificaciones: str = None,
                                     id_proveedor: int = None, id_precio_compra: int = None,
                                     id_color: int = None) -> Dict[str, Any]:
        """
        Crear un producto simple completo con todas sus relaciones
        
        Returns:
            Dict[str, Any]: Diccionario con producto y producto_simple creados
        """
        try:
            # Crear el producto base
            producto = self.crear(tipo_producto='simple', id_articulo=id_articulo)
            
            # Crear el producto simple
            producto_simple = ProductoSimple(
                id_producto=producto.id,
                especificaciones=especificaciones,
                id_proveedor=id_proveedor,
                id_precio_compra=id_precio_compra,
                id_color=id_color
            )
            
            self.db.add(producto_simple)
            self.db.commit()
            self.db.refresh(producto_simple)
            
            logger.info(f"✅ Producto simple completo creado para artículo {id_articulo}")
            # Crear un stock vacío para el producto simple
            stock = Stock(
                id_producto_simple=producto.id,
                cantidad_actual=Decimal('0')
            )
            self.db.add(stock)
            self.db.commit()
            self.db.refresh(stock)

            return {
                'producto': producto,
                'producto_simple': producto_simple,
                'stock': stock
            }
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error creando producto simple: {e}")
            raise
            
    def crear_producto_compuesto_completo(self, id_articulo: int, 
                                        descripcion_compuesto: str = None) -> Dict[str, Any]:
        """
        Crear un producto compuesto completo
        
        Returns:
            Dict[str, Any]: Diccionario con producto y producto_compuesto creados
        """
        try:
            # Crear el producto base
            producto = self.crear(tipo_producto='compuesto', id_articulo=id_articulo)
            
            # Crear el producto compuesto
            producto_compuesto = ProductoCompuesto(
                id_producto=producto.id,
                descripcion_compuesto=descripcion_compuesto
            )
            
            self.db.add(producto_compuesto)
            self.db.commit()
            self.db.refresh(producto_compuesto)
            
            logger.info(f"✅ Producto compuesto completo creado para artículo {id_articulo}")
            return {
                'producto': producto,
                'producto_compuesto': producto_compuesto
            }
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error creando producto compuesto: {e}")
            raise
            
    def obtener_producto_simple(self, producto_id: int) -> Optional[ProductoSimple]:
        """Obtener el detalle de producto simple por ID de producto"""
        try:
            return self.db.query(ProductoSimple).filter(
                ProductoSimple.id_producto == producto_id
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo producto simple {producto_id}: {e}")
            raise
            
    def obtener_producto_compuesto(self, producto_id: int) -> Optional[ProductoCompuesto]:
        """Obtener el detalle de producto compuesto por ID de producto"""
        try:
            return self.db.query(ProductoCompuesto).filter(
                ProductoCompuesto.id_producto == producto_id
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo producto compuesto {producto_id}: {e}")
            raise
            
    def agregar_componente_a_producto(self, id_producto_compuesto: int, 
                                    id_componente: int, cantidad_necesaria: float) -> ComponenteProducto:
        """
        Agregar un componente a un producto compuesto
        """
        try:
            # Verificar que es un producto compuesto
            producto_compuesto = self.db.query(ProductoCompuesto).filter(
                ProductoCompuesto.id == id_producto_compuesto
            ).first()
            
            if not producto_compuesto:
                raise ValueError(f"Producto compuesto {id_producto_compuesto} no encontrado")
                
            componente_producto = ComponenteProducto(
                id_componente=id_componente,
                id_producto_compuesto=id_producto_compuesto,
                cantidad_necesaria=Decimal(cantidad_necesaria)
            )
            
            self.db.add(componente_producto)
            self.db.commit()
            self.db.refresh(componente_producto)
            
            logger.info(f"✅ Componente {id_componente} agregado a producto compuesto {id_producto_compuesto}")
            return componente_producto
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error agregando componente a producto: {e}")
            raise
            
    def calcular_costo_producto_compuesto(self, producto_compuesto_id: int) -> Dict[str, Any]:
        """
        Calcular el costo total de un producto compuesto basado en sus componentes
        """
        try:
            componentes_productos = self.db.query(ComponenteProducto).filter(
                ComponenteProducto.id_producto_compuesto == producto_compuesto_id
            ).all()
            
            if not componentes_productos:
                return {'costo_total': 0, 'componentes': [], 'moneda': 'EUR'}
                
            costo_total = Decimal('0')
            detalles_componentes = []
            moneda_base = 'EUR'
            
            for cp in componentes_productos:
                componente = cp.componente
                if componente.precio_compra:
                    costo_componente = componente.precio_compra.valor * cp.cantidad_necesaria
                    costo_total += costo_componente
                    
                    detalles_componentes.append({
                        'componente_id': componente.id,
                        'nombre': componente.nombre,
                        'cantidad_necesaria': float(cp.cantidad_necesaria),
                        'precio_unitario': float(componente.precio_compra.valor),
                        'costo_total': float(costo_componente),
                        'moneda': componente.precio_compra.moneda
                    })
                    
            return {
                'costo_total': float(costo_total),
                'componentes': detalles_componentes,
                'moneda': moneda_base,
                'total_componentes': len(componentes_productos)
            }
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error calculando costo de producto compuesto {producto_compuesto_id}: {e}")
            raise
            
    def verificar_disponibilidad_fabricacion(self, producto_compuesto_id: int, 
                                           cantidad_deseada: int = 1) -> Dict[str, Any]:
        """
        Verificar si se puede fabricar una cantidad específica de un producto compuesto
        """
        try:
            componentes_productos = self.db.query(ComponenteProducto).filter(
                ComponenteProducto.id_producto_compuesto == producto_compuesto_id
            ).all()
            
            puede_fabricar = True
            detalles_componentes = []
            faltantes = []
            
            for cp in componentes_productos:
                cantidad_necesaria_total = cp.cantidad_necesaria * cantidad_deseada
                stock_componente = self.db.query(Stock).filter(
                    Stock.id_componente == cp.id_componente
                ).first()
                
                cantidad_disponible = float(stock_componente.cantidad_actual) if stock_componente else 0
                suficiente = cantidad_disponible >= cantidad_necesaria_total
                
                if not suficiente:
                    puede_fabricar = False
                    faltantes.append({
                        'componente_id': cp.id_componente,
                        'nombre': cp.componente.nombre,
                        'cantidad_necesaria': float(cantidad_necesaria_total),
                        'cantidad_disponible': cantidad_disponible,
                        'cantidad_faltante': float(cantidad_necesaria_total - cantidad_disponible)
                    })
                    
                detalles_componentes.append({
                    'componente_id': cp.id_componente,
                    'nombre': cp.componente.nombre,
                    'cantidad_necesaria': float(cantidad_necesaria_total),
                    'cantidad_disponible': cantidad_disponible,
                    'suficiente': suficiente
                })
                
            return {
                'puede_fabricar': puede_fabricar,
                'cantidad_deseada': cantidad_deseada,
                'detalles_componentes': detalles_componentes,
                'componentes_faltantes': faltantes,
                'total_componentes': len(componentes_productos)
            }
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error verificando disponibilidad de fabricación: {e}")
            raise
            
    def obtener_productos_por_tipo(self, tipo_producto: str) -> List[Producto]:
        """
        Obtener productos filtrados por tipo ('simple' o 'compuesto')
        """
        try:
            return self.db.query(Producto).filter(
                Producto.tipo_producto == tipo_producto
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo productos por tipo {tipo_producto}: {e}")
            raise
