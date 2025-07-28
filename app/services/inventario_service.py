"""
🎯 Servicio de Inventario - Coordinador principal de todos los servicios

Este servicio actúa como el coordinador principal que utiliza todos los demás servicios
para realizar operaciones complejas que involucran múltiples entidades.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .familia_service import FamiliaService
from .color_service import ColorService
from .proveedor_service import ProveedorService
from .precio_service import PrecioService
from .articulo_service import ArticuloService
from .producto_service import ProductoService
from .componente_service import ComponenteService
from .pack_service import PackService
from .stock_service import StockService

import logging

logger = logging.getLogger(__name__)


class InventarioService:
    """
    🎯 Servicio principal de inventario
    
    Coordina todos los servicios especializados para realizar operaciones
    complejas que involucran múltiples entidades del sistema.
    """
    
    def __init__(self, db_session: Session):
        """
        Constructor del servicio principal de inventario
        
        Args:
            db_session (Session): Sesión de base de datos SQLAlchemy
        """
        self.db = db_session
        
        # Inicializar todos los servicios especializados
        self.familia_service = FamiliaService(db_session)
        self.color_service = ColorService(db_session)
        self.proveedor_service = ProveedorService(db_session)
        self.precio_service = PrecioService(db_session)
        self.articulo_service = ArticuloService(db_session)
        self.producto_service = ProductoService(db_session)
        self.componente_service = ComponenteService(db_session)
        self.pack_service = PackService(db_session)
        self.stock_service = StockService(db_session)
        
    def crear_producto_simple_completo(self, nombre_articulo: str, descripcion_articulo: str = None,
                                     codigo_articulo: str = None, familia_id: int = None,
                                     precio_venta: float = None, precio_compra: float = None,
                                     proveedor_id: int = None, color_id: int = None,
                                     especificaciones: str = None, stock_inicial: float = 0,
                                     stock_minimo: float = 0, ubicacion_almacen: str = None) -> Dict[str, Any]:
        """
        Crear un producto simple completo con todos sus elementos relacionados
        
        Esta operación crea en una sola transacción:
        - Precio de venta (si se proporciona)
        - Precio de compra (si se proporciona)
        - Artículo
        - Producto y ProductoSimple
        - Stock inicial
        """
        try:
            resultado = {}
            
            # 1. Crear precio de venta si se proporciona
            if precio_venta:
                precio_venta_obj = self.precio_service.crear_precio_venta(precio_venta)
                resultado['precio_venta'] = precio_venta_obj
            else:
                precio_venta_obj = None
                
            # 2. Crear precio de compra si se proporciona
            if precio_compra:
                precio_compra_obj = self.precio_service.crear_precio_compra(precio_compra)
                resultado['precio_compra'] = precio_compra_obj
            else:
                precio_compra_obj = None
                
            # 3. Crear artículo
            articulo = self.articulo_service.crear_articulo(
                nombre=nombre_articulo,
                descripcion=descripcion_articulo,
                codigo=codigo_articulo,
                id_familia=familia_id,
                id_precio_venta=precio_venta_obj.id if precio_venta_obj else None
            )
            resultado['articulo'] = articulo
            
            # 4. Crear producto simple
            producto_data = self.producto_service.crear_producto_simple_completo(
                id_articulo=articulo.id,
                especificaciones=especificaciones,
                id_proveedor=proveedor_id,
                id_precio_compra=precio_compra_obj.id if precio_compra_obj else None,
                id_color=color_id
            )
            resultado.update(producto_data)
            
            # 5. Crear stock inicial
            from app.models.stock import Stock
            stock = Stock(
                cantidad_actual=stock_inicial,
                cantidad_minima=stock_minimo,
                ubicacion_almacen=ubicacion_almacen,
                id_producto_simple=producto_data['producto_simple'].id
            )
            
            self.db.add(stock)
            self.db.commit()
            self.db.refresh(stock)
            resultado['stock'] = stock
            
            logger.info(f"✅ Producto simple completo '{nombre_articulo}' creado exitosamente")
            return resultado
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creando producto simple completo: {e}")
            raise
            
    def crear_producto_compuesto_completo(self, nombre_articulo: str, descripcion_articulo: str = None,
                                        codigo_articulo: str = None, familia_id: int = None,
                                        precio_venta: float = None, descripcion_compuesto: str = None,
                                        componentes_necesarios: List[Dict] = None) -> Dict[str, Any]:
        """
        Crear un producto compuesto completo con componentes
        
        Args:
            componentes_necesarios: Lista de dicts con 'id_componente' y 'cantidad_necesaria'
        """
        try:
            resultado = {}
            
            # 1. Crear precio de venta si se proporciona
            if precio_venta:
                precio_venta_obj = self.precio_service.crear_precio_venta(precio_venta)
                resultado['precio_venta'] = precio_venta_obj
            else:
                precio_venta_obj = None
                
            # 2. Crear artículo
            articulo = self.articulo_service.crear_articulo(
                nombre=nombre_articulo,
                descripcion=descripcion_articulo,
                codigo=codigo_articulo,
                id_familia=familia_id,
                id_precio_venta=precio_venta_obj.id if precio_venta_obj else None
            )
            resultado['articulo'] = articulo
            
            # 3. Crear producto compuesto
            producto_data = self.producto_service.crear_producto_compuesto_completo(
                id_articulo=articulo.id,
                descripcion_compuesto=descripcion_compuesto
            )
            resultado.update(producto_data)
            
            # 4. Agregar componentes si se proporcionan
            componentes_agregados = []
            if componentes_necesarios:
                for comp_info in componentes_necesarios:
                    comp_producto = self.producto_service.agregar_componente_a_producto(
                        id_producto_compuesto=producto_data['producto_compuesto'].id,
                        id_componente=comp_info['id_componente'],
                        cantidad_necesaria=comp_info['cantidad_necesaria']
                    )
                    componentes_agregados.append(comp_producto)
                    
            resultado['componentes_agregados'] = componentes_agregados
            
            logger.info(f"✅ Producto compuesto '{nombre_articulo}' creado con {len(componentes_agregados)} componentes")
            return resultado
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creando producto compuesto completo: {e}")
            raise
            
    def crear_pack_completo(self, nombre_pack: str, descripcion_articulo: str = None,
                          codigo_articulo: str = None, familia_id: int = None,
                          precio_venta: float = None, descripcion_pack: str = None,
                          descuento_porcentaje: int = 0, productos_incluidos: List[Dict] = None) -> Dict[str, Any]:
        """
        Crear un pack completo con productos incluidos
        """
        try:
            resultado = {}
            
            # 1. Crear precio de venta si se proporciona
            if precio_venta:
                precio_venta_obj = self.precio_service.crear_precio_venta(precio_venta)
                resultado['precio_venta'] = precio_venta_obj
            else:
                precio_venta_obj = None
                
            # 2. Crear artículo
            articulo = self.articulo_service.crear_articulo(
                nombre=nombre_pack,
                descripcion=descripcion_articulo,
                codigo=codigo_articulo,
                id_familia=familia_id,
                id_precio_venta=precio_venta_obj.id if precio_venta_obj else None
            )
            resultado['articulo'] = articulo
            
            # 3. Crear pack completo
            pack_data = self.pack_service.crear_pack_completo(
                nombre=nombre_pack,
                id_articulo=articulo.id,
                descripcion=descripcion_pack,
                descuento_porcentaje=descuento_porcentaje,
                productos_incluidos=productos_incluidos
            )
            resultado.update(pack_data)
            
            logger.info(f"✅ Pack completo '{nombre_pack}' creado exitosamente")
            return resultado
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creando pack completo: {e}")
            raise
            
    def obtener_dashboard_inventario(self) -> Dict[str, Any]:
        """
        Obtener un dashboard completo del estado del inventario
        """
        try:
            return {
                'resumen_stock': self.stock_service.obtener_resumen_inventario(),
                'alertas_reposicion': len(self.stock_service.obtener_stock_bajo_minimo()),
                'total_familias': self.familia_service.contar(),
                'total_proveedores': self.proveedor_service.contar(),
                'total_articulos': self.articulo_service.contar(),
                'total_productos': self.producto_service.contar(),
                'total_componentes': self.componente_service.contar(),
                'total_packs': self.pack_service.contar(),
                'productos_simples': len(self.producto_service.obtener_productos_por_tipo('simple')),
                'productos_compuestos': len(self.producto_service.obtener_productos_por_tipo('compuesto'))
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo dashboard de inventario: {e}")
            raise
            
    def buscar_elementos_inventario(self, texto_busqueda: str) -> Dict[str, List]:
        """
        Búsqueda global en todos los elementos del inventario
        """
        try:
            return {
                'familias': self.familia_service.buscar_familias_por_texto(texto_busqueda),
                'colores': self.color_service.buscar_colores_por_texto(texto_busqueda),
                'proveedores': self.proveedor_service.buscar_proveedores_por_texto(texto_busqueda),
                'articulos': self.articulo_service.buscar_articulos_por_texto(texto_busqueda),
                'componentes': [c for c in self.componente_service.obtener_todos() 
                              if texto_busqueda.lower() in c.nombre.lower()]
            }
            
        except Exception as e:
            logger.error(f"❌ Error en búsqueda global: {e}")
            raise
