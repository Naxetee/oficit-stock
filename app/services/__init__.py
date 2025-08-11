def get_FamiliaService():
    from .familia_service import FamiliaService
    return FamiliaService

def get_PackService():
    from .pack_service import PackService
    return PackService

def get_ProductoCompuestoService():
    from .producto_compuesto_service import ProductoCompuestoService
    return ProductoCompuestoService

def get_ProductoSimpleService():
    from .producto_simple_service import ProductoSimpleService
    return ProductoSimpleService

def get_ProveedorService():
    from .proveedor_service import ProveedorService
    return ProveedorService

def get_ColorService():
    from .color_service import ColorService
    return ColorService

def get_ComponenteService():
    from .componente_service import ComponenteService
    return ComponenteService

def get_StockService():
    from .stock_service import StockService
    return StockService

def get_MovimientoService():
    from .movimiento_service import MovimientoService
    return MovimientoService