# 🛠️ Servicios de Negocio - Sistema de Inventario

"""
Este módulo contiene todos los servicios de negocio del sistema de inventario.
Cada servicio se enfoca en las operaciones específicas de un modelo o grupo de modelos relacionados.

Servicios disponibles:
- FamiliaService: Gestión de familias de productos
- ColorService: Gestión de colores
- ProveedorService: Gestión de proveedores
- PrecioService: Gestión de precios de venta y compra
- ArticuloService: Gestión de artículos
- ProductoService: Gestión de productos (simples y compuestos)
- ComponenteService: Gestión de componentes
- PackService: Gestión de packs
- StockService: Gestión de inventario y stock
- InventarioService: Servicio principal que coordina todos los demás
"""

from .familia_service import FamiliaService
from .color_service import ColorService
from .proveedor_service import ProveedorService
from .precio_service import PrecioService
from .articulo_service import ArticuloService
from .producto_service import ProductoService
from .componente_service import ComponenteService
from .pack_service import PackService
from .stock_service import StockService
from .inventario_service import InventarioService

__all__ = [
    'FamiliaService',
    'ColorService', 
    'ProveedorService',
    'PrecioService',
    'ArticuloService',
    'ProductoService',
    'ComponenteService',
    'PackService',
    'StockService',
    'InventarioService'
]
