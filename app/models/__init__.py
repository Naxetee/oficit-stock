# Models package
# This package contains all database models for the inventory system

# Entidades principales
from .familia import Familia
from .color import Color
from .proveedor import Proveedor
from .precio_venta import PrecioVenta
from .precio_compra import PrecioCompra
from .articulo import Articulo
from .producto import Producto
from .producto_simple import ProductoSimple
from .producto_compuesto import ProductoCompuesto
from .componente import Componente
from .pack import Pack
from .stock import Stock

# Tablas intermedias
from .componente_producto import ComponenteProducto
from .pack_producto import PackProducto

# Exportar todos los modelos
__all__ = [
    "Familia",
    "Color", 
    "Proveedor",
    "PrecioVenta",
    "PrecioCompra",
    "Articulo",
    "Producto",
    "ProductoSimple",
    "ProductoCompuesto",
    "Componente",
    "Pack",
    "Stock",
    "ComponenteProducto",
    "PackProducto",
    "InventarioService"
]
