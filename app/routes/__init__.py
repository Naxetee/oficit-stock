"""
🚀 Módulo de Rutas del Sistema de Inventario

Este módulo contiene todas las rutas organizadas por modelo,
proporcionando endpoints RESTful para cada entidad del sistema.
"""

from .familia_routes import router as familia_router
from .color_routes import router as color_router
from .proveedor_routes import router as proveedor_router
from .articulo_routes import router as articulo_router
from .componente_routes import router as componente_router
from .producto_routes import router as producto_router
from .pack_routes import router as pack_router
from .stock_routes import router as stock_router
from .inventario_routes import router as inventario_router

__all__ = [
    "familia_router",
    "color_router", 
    "proveedor_router",
    "articulo_router",
    "componente_router",
    "producto_router",
    "pack_router",
    "stock_router",
    "inventario_router"
]
