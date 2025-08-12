from sqladmin import ModelView
from app.models.componente_model import Componente
from app.models.pack_model import Pack
from app.models.stock_model import Stock
from app.models.composicion_prod_compuesto_model import ComposicionProdCompuesto as ComposicionProdCompuestoModel
from app.models.articulo_model import Articulo
from app.models.familia_model import Familia
from app.models.proveedor_model import Proveedor
from app.models.color_model import Color
from app.models.producto_compuesto_model import ProductoCompuesto
from app.models.producto_simple_model import ProductoSimple
from app.models.composicion_pack_model import ComposicionPack

from app.schemas.componente_schema import ComponenteCreate
from app.schemas.pack_schema import PackCreate
from app.schemas.stock_schema import StockCreate
from app.schemas.composicion_producto_compuesto_schema import ComposicionProdCompuestoCreate
from app.schemas.articulo_schema import ArticuloCreate
from app.schemas.familia_schema import FamiliaCreate
from app.schemas.proveedor_schema import ProveedorCreate
from app.schemas.color_schema import ColorCreate

def _schema_fields(schema_cls):
    return list(getattr(schema_cls, "model_fields", getattr(schema_cls, "__fields__", {})).keys())

class ComponenteAdmin(ModelView, model=Componente):
    name = "Componente"
    column_list = [c.name for c in Componente.__table__.columns]
    form_columns = _schema_fields(ComponenteCreate)
    icon = "fa-solid fa-cube"

class StockAdmin(ModelView, model=Stock):
    name = "Stock"
    column_list = [c.name for c in Stock.__table__.columns]
    form_columns = _schema_fields(StockCreate)
    icon = "fa-solid fa-boxes-stacked"

class ComposicionProdCompuestoAdmin(ModelView, model=ComposicionProdCompuestoModel):
    name = "Composición Producto Compuesto"
    column_list = ["cantidad", "Componente_", "Producto_Compuesto"]
    form_columns = ["cantidad", "Componente_", "Producto_Compuesto"]
    icon = "fa-solid fa-layer-group"

class ComposicionPackAdmin(ModelView, model=ComposicionPack):
    name = "Composición Pack"
    column_list = ["cantidad", "Producto_", "Pack_"]
    form_columns = ["cantidad", "Producto_", "Pack_"]
    icon = "fa-solid fa-layer-group"

class ArticuloAdmin(ModelView, model=Articulo):
    name = "Artículo"
    column_list = [c.name for c in Articulo.__table__.columns]
    form_columns = _schema_fields(ArticuloCreate)
    icon = "fa-solid fa-tag"

class FamiliaAdmin(ModelView, model=Familia):
    name = "Familia"
    column_list = [c.name for c in Familia.__table__.columns]
    form_columns = _schema_fields(FamiliaCreate)
    icon = "fa-solid fa-sitemap"

class ProveedorAdmin(ModelView, model=Proveedor):
    name = "Proveedor"
    column_list = [c.name for c in Proveedor.__table__.columns]
    form_columns = _schema_fields(ProveedorCreate)
    icon = "fa-solid fa-truck"

class ColorAdmin(ModelView, model=Color):
    name = "Color"
    column_list = [c.name for c in Color.__table__.columns]
    form_columns = _schema_fields(ColorCreate)
    icon = "fa-solid fa-palette"

class PackAdmin(ModelView, model=Pack):
    name = "Pack"
    column_list = [c.name for c in Pack.__table__.columns]
    form_columns = _schema_fields(PackCreate)
    icon = "fa-solid fa-box"

class ProductoCompuestoAdmin(ModelView, model=ProductoCompuesto):
    name = "Producto Compuesto"
    column_list = [c.name for c in ProductoCompuesto.__table__.columns]
    form_columns = [c.name for c in ProductoCompuesto.__table__.columns]
    icon = "fa-solid fa-cubes"

class ProductoSimpleAdmin(ModelView, model=ProductoSimple):
    name = "Producto Simple"
    column_list = [c.name for c in ProductoSimple.__table__.columns]
    form_columns = [c.name for c in ProductoSimple.__table__.columns]
    icon = "fa-solid fa-cube"

def register_admin_views(admin):
    admin.add_view(ComponenteAdmin)
    admin.add_view(StockAdmin)
    admin.add_view(ComposicionProdCompuestoAdmin)
    admin.add_view(ComposicionPackAdmin)
    admin.add_view(ArticuloAdmin)
    admin.add_view(FamiliaAdmin)
    admin.add_view(ProveedorAdmin)
    admin.add_view(ColorAdmin)
    admin.add_view(PackAdmin)
    admin.add_view(ProductoCompuestoAdmin)
    admin.add_view(ProductoSimpleAdmin)
