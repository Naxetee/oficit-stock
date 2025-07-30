# Schemas package
# This package contains all Pydantic schemas for request/response validation

from .familiaDTO import FamiliaBase, FamiliaCreate, FamiliaUpdate, FamiliaInDB, FamiliaResponse
from .categoriaDTO import CategoriaBase, CategoriaCreate, CategoriaUpdate, CategoriaInDB, CategoriaResponse
from .proveedorDTO import ProveedorBase, ProveedorCreate, ProveedorUpdate, ProveedorInDB, ProveedorResponse
from .articuloDTO import ArticuloBase, ArticuloCreate, ArticuloUpdate, ArticuloInDB, ArticuloResponse
from .colorDTO import ColorBase, ColorCreate, ColorUpdate, ColorInDB, ColorResponse
from .inventarioDTO import (
    MovimientoInventarioBase, 
    MovimientoInventarioCreate, 
    MovimientoInventarioUpdate, 
    MovimientoInventarioInDB, 
    MovimientoInventarioResponse,
    InventarioResumen
)

__all__ = [
    "FamiliaBase", "FamiliaCreate", "FamiliaUpdate", "FamiliaInDB", "FamiliaResponse",
    "CategoriaBase", "CategoriaCreate", "CategoriaUpdate", "CategoriaInDB", "CategoriaResponse",
    "ProveedorBase", "ProveedorCreate", "ProveedorUpdate", "ProveedorInDB", "ProveedorResponse",
    "ArticuloBase", "ArticuloCreate", "ArticuloUpdate", "ArticuloInDB", "ArticuloResponse",
    "ColorBase", "ColorCreate", "ColorUpdate", "ColorInDB", "ColorResponse",
    "MovimientoInventarioBase", "MovimientoInventarioCreate", "MovimientoInventarioUpdate", 
    "MovimientoInventarioInDB", "MovimientoInventarioResponse", "InventarioResumen"
]
