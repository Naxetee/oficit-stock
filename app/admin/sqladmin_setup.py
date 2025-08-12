from sqladmin import ModelView
from app.models.componente_model import Componente
from app.models.stock_model import Stock
from app.models.composicion_prod_compuesto_model import ComposicionProdCompuesto as ComposicionProdCompuestoModel
from app.models.articulo_model import Articulo
from app.models.familia_model import Familia
from app.models.proveedor_model import Proveedor
from app.models.color_model import Color

from app.schemas.componente_schema import ComponenteCreate
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
    # Mostrar cantidad, el objeto componente y el objeto producto compuesto
    column_list = ["cantidad", "Componente_", "Producto_Compuesto"]
    form_columns = ["cantidad", "Componente_", "Producto_Compuesto"]
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

def register_admin_views(admin):
    admin.add_view(ComponenteAdmin)
    admin.add_view(StockAdmin)
    admin.add_view(ComposicionProdCompuestoAdmin)
    admin.add_view(ArticuloAdmin)
    admin.add_view(FamiliaAdmin)
    admin.add_view(ProveedorAdmin)
    admin.add_view(ColorAdmin)
