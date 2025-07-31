# Models package
# This package contains all database models for the inventory system

# Entidades principales
from .familia import Familia
from .color import Color
from .proveedor import Proveedor
from .articulo import Articulo
from .componente import Componente
from .producto import Producto
from .producto_simple import ProductoSimple
from .producto_compuesto import ProductoCompuesto
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
    "Articulo",
    "Componente",
    "Producto",
    "ProductoSimple",
    "ProductoCompuesto",
    "Pack",
    "Stock",
    "ComponenteProducto",
    "PackProducto",
    "InventarioService"
]
