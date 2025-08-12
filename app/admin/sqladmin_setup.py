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

def _model_fields(model_cls):
    # Devuelve todos los nombres de columnas salvo created_at y updated_at
    return [c.name for c in model_cls.__table__.columns if c.name not in ("created_at", "updated_at")]

# Personalización de la cabecera del panel de administración
class CustomAdmin(Admin):
    title = "Panel de Inventario"
    description = "Bienvenido al sistema de gestión de inventario. Administra productos, componentes y más."
    logo_url = "/static/logo.svg"
    favicon_url = "/static/favicon.ico"

class ComponenteAdmin(ModelView, model=Componente):
    name = "Componente"
    description = "Gestión de componentes individuales del inventario."
    column_list = [c.name for c in Componente.__table__.columns]
    form_columns = _model_fields(Componente)
    icon = "fa-solid fa-cube"

class StockAdmin(ModelView, model=Stock):
    name = "Stock"
    description = "Control y seguimiento de existencias."
    column_list = [c.name for c in Stock.__table__.columns]
    form_columns = _model_fields(Stock)
    icon = "fa-solid fa-boxes-stacked"

class ComposicionProdCompuestoAdmin(ModelView, model=ComposicionProdCompuestoModel):
    name = "Composición Producto Compuesto"
    description = "Relación entre productos compuestos y sus componentes."
    column_list = ["cantidad", "Componente_", "Producto_Compuesto"]
    form_columns = _model_fields(ComposicionProdCompuestoModel)
    icon = "fa-solid fa-layer-group"

class ComposicionPackAdmin(ModelView, model=ComposicionPack):
    name = "Composición Pack"
    description = "Gestión de la composición de los packs."
    column_list = ["cantidad", "Producto_", "Pack_"]
    form_columns = _model_fields(ComposicionPack)
    icon = "fa-solid fa-layer-group"

class ArticuloAdmin(ModelView, model=Articulo):
    name = "Artículo"
    description = "Artículos disponibles en el inventario."
    column_list = [c.name for c in Articulo.__table__.columns]
    form_columns = _model_fields(Articulo)
    icon = "fa-solid fa-tag"

class FamiliaAdmin(ModelView, model=Familia):
    name = "Familia"
    description = "Clasificación de artículos por familias."
    column_list = [c.name for c in Familia.__table__.columns]
    form_columns = _model_fields(Familia)
    icon = "fa-solid fa-sitemap"

class ProveedorAdmin(ModelView, model=Proveedor):
    name = "Proveedor"
    description = "Gestión de proveedores."
    column_list = [c.name for c in Proveedor.__table__.columns]
    form_columns = _model_fields(Proveedor)
    icon = "fa-solid fa-truck"

class ColorAdmin(ModelView, model=Color):
    name = "Color"
    description = "Colores disponibles para los productos."
    column_list = [c.name for c in Color.__table__.columns]
    form_columns = _model_fields(Color)
    icon = "fa-solid fa-palette"

class PackAdmin(ModelView, model=Pack):
    name = "Pack"
    description = "Gestión de packs de productos."
    column_list = [c.name for c in Pack.__table__.columns]
    form_columns = _model_fields(Pack)
    icon = "fa-solid fa-box"

class ProductoCompuestoAdmin(ModelView, model=ProductoCompuesto):
    name = "Producto Compuesto"
    description = "Productos compuestos por varios componentes."
    column_list = [c.name for c in ProductoCompuesto.__table__.columns]
    form_columns = _model_fields(ProductoCompuesto)
    icon = "fa-solid fa-cubes"

class ProductoSimpleAdmin(ModelView, model=ProductoSimple):
    name = "Producto Simple"
    description = "Productos simples del inventario."
    column_list = [c.name for c in ProductoSimple.__table__.columns]
    form_columns = _model_fields(ProductoSimple)
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

