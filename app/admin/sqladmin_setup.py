from sqladmin import ModelView, Admin
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

# Import schemas
from app.schemas.componente_schema import ComponenteResponse, ComponenteCreate, ComponenteUpdate
from app.schemas.stock_schema import StockResponse, StockCreate, StockUpdate
from app.schemas.composicion_producto_compuesto_schema import ComposicionProdCompuesto, ComposicionProdCompuestoCreate
from app.schemas.composicion_pack_schema import ComposicionPackResponse, ComposicionPackCreate
from app.schemas.articulo_schema import ArticuloResponse, ArticuloCreate, ArticuloUpdate
from app.schemas.familia_schema import FamiliaResponse, FamiliaCreate, FamiliaUpdate
from app.schemas.proveedor_schema import ProveedorResponse, ProveedorCreate, ProveedorUpdate
from app.schemas.color_schema import ColorResponse, ColorCreate, ColorUpdate
from app.schemas.pack_schema import PackResponse, PackCreate, PackUpdate
from app.schemas.producto_compuesto_schema import ProductoCompuestoResponse, ProductoCompuestoCreate, ProductoCompuestoUpdate
from app.schemas.producto_simple_schema import ProductoSimpleResponse, ProductoSimpleCreate, ProductoSimpleUpdate

def read_fields(schema_cls):
    return list(schema_cls.model_fields.keys())

def create_fields(schema_cls):
    return list(schema_cls.model_fields.keys())

def update_fields(schema_cls):
    return list(schema_cls.model_fields.keys())

class CustomAdmin(Admin):
    title = "Panel de Inventario"
    description = "Bienvenido al sistema de gestión de inventario. Administra productos, componentes y más."
    favicon_url = "/static/favicon.ico"
    head_template = "admin/head.html"

class ComponenteAdmin(ModelView, model=Componente):
    name = "Componente"
    description = "Gestión de componentes individuales del inventario."
    column_list = read_fields(ComponenteResponse)
    form_columns = create_fields(ComponenteCreate)
    form_edit_columns = update_fields(ComponenteUpdate)
    icon = "fa-solid fa-cube"

class StockAdmin(ModelView, model=Stock):
    name = "Stock"
    description = "Control y seguimiento de existencias."
    column_list = read_fields(StockResponse)
    form_columns = create_fields(StockCreate)
    form_edit_columns = update_fields(StockUpdate)
    icon = "fa-solid fa-boxes-stacked"

class ComposicionProdCompuestoAdmin(ModelView, model=ComposicionProdCompuestoModel):
    name = "Composición Producto Compuesto"
    description = "Relación entre productos compuestos y sus componentes."
    column_list = read_fields(ComposicionProdCompuesto)
    form_columns = create_fields(ComposicionProdCompuestoCreate)
    form_edit_columns = update_fields(ComposicionProdCompuestoCreate)
    icon = "fa-solid fa-layer-group"

class ComposicionPackAdmin(ModelView, model=ComposicionPack):
    name = "Composición Pack"
    description = "Gestión de la composición de los packs."
    column_list = read_fields(ComposicionPackResponse)
    form_columns = create_fields(ComposicionPackCreate)
    form_edit_columns = update_fields(ComposicionPackCreate)
    icon = "fa-solid fa-layer-group"

class ArticuloAdmin(ModelView, model=Articulo):
    name = "Artículo"
    description = "Artículos disponibles en el inventario."
    column_list = read_fields(ArticuloResponse)
    form_columns = create_fields(ArticuloCreate)
    form_edit_columns = update_fields(ArticuloUpdate)
    icon = "fa-solid fa-tag"

class FamiliaAdmin(ModelView, model=Familia):
    name = "Familia"
    description = "Clasificación de artículos por familias."
    column_list = read_fields(FamiliaResponse)
    form_columns = create_fields(FamiliaCreate)
    form_edit_columns = update_fields(FamiliaUpdate)
    icon = "fa-solid fa-sitemap"

class ProveedorAdmin(ModelView, model=Proveedor):
    name = "Proveedor"
    description = "Gestión de proveedores."
    column_list = read_fields(ProveedorResponse)
    form_columns = create_fields(ProveedorCreate)
    form_edit_columns = update_fields(ProveedorUpdate)
    icon = "fa-solid fa-truck"

class ColorAdmin(ModelView, model=Color):
    name = "Color"
    description = "Colores disponibles para los productos."
    column_list = read_fields(ColorResponse)
    form_columns = create_fields(ColorCreate)
    form_edit_columns = update_fields(ColorUpdate)
    icon = "fa-solid fa-palette"

class PackAdmin(ModelView, model=Pack):
    name = "Pack"
    description = "Gestión de packs de productos."
    column_list = read_fields(PackResponse)
    form_columns = create_fields(PackCreate)
    form_edit_columns = update_fields(PackUpdate)
    icon = "fa-solid fa-box"

class ProductoCompuestoAdmin(ModelView, model=ProductoCompuesto):
    name = "Producto Compuesto"
    description = "Productos compuestos por varios componentes."
    column_list = read_fields(ProductoCompuestoResponse)
    form_columns = create_fields(ProductoCompuestoCreate)
    form_edit_columns = update_fields(ProductoCompuestoUpdate)
    icon = "fa-solid fa-cubes"

class ProductoSimpleAdmin(ModelView, model=ProductoSimple):
    name = "Producto Simple"
    description = "Productos simples del inventario."
    column_list = read_fields(ProductoSimpleResponse)
    form_columns = create_fields(ProductoSimpleCreate)
    form_edit_columns = update_fields(ProductoSimpleUpdate)
    icon = "fa-solid fa-cube"

def register_admin_views(admin):
    admin.add_view(StockAdmin)
    admin.add_view(ArticuloAdmin)
    admin.add_view(ProductoSimpleAdmin)
    admin.add_view(ProductoCompuestoAdmin)
    admin.add_view(ComponenteAdmin)
    admin.add_view(ComposicionProdCompuestoAdmin)
    admin.add_view(PackAdmin)
    admin.add_view(ComposicionPackAdmin)
    admin.add_view(ProveedorAdmin)
    admin.add_view(FamiliaAdmin)
    admin.add_view(ColorAdmin)
