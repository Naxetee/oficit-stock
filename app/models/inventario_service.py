from sqlalchemy import DateTime, func
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models import *

class InventarioService:
    """
    Servicio para manejar operaciones complejas del inventario
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    # Operaciones de precios
    def crear_precio_venta(self, valor: float, moneda: str = 'EUR', fecha_inicio: Optional[DateTime] = None, fecha_fin: Optional[DateTime] = None) -> PrecioVenta:
        """Crea un nuevo precio de venta"""
        precio_venta = PrecioVenta(valor=valor, moneda=moneda, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        self.db.add(precio_venta)
        self.db.flush()
        return precio_venta

    def crear_precio_compra(self, valor: float, moneda: str = 'EUR', fecha_inicio: Optional[DateTime] = None, fecha_fin: Optional[DateTime] = None) -> PrecioCompra:
        """Crea un nuevo precio de compra"""
        precio_compra = PrecioCompra(valor=valor, moneda=moneda, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        self.db.add(precio_compra)
        self.db.flush()
        return precio_compra

    # Operaciones de color
    def crear_color(self, nombre: str, url_imagen: Optional[str] = None, activo: bool = True, id_familia: Optional[int] = None) -> Color:
        """Crea un nuevo color"""
        color = Color(nombre=nombre, url_imagen=url_imagen, activo=activo, id_familia=id_familia)
        self.db.add(color)
        self.db.flush()
        return color
    
    # Operaciones de Stock

    # Operaciones de Artículo
    def crear_articulo_producto_simple(
        self, 
        nombre_articulo: str,
        id_familia: int,
        id_proveedor: int,
        id_precio_venta: int,
        id_precio_compra: int,
        id_color: Optional[int],
        activo: bool = True,
        descripcion: Optional[str] = None,
        sku: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Crea un artículo con producto simple de forma completa"""

        # Crear artículo
        articulo = Articulo(
            nombre=nombre_articulo,
            descripcion=descripcion,
            sku=sku,
            activo=activo,
            id_familia=id_familia,
            id_precio_venta=id_precio_venta
        )
        self.db.add(articulo)
        self.db.flush()
        
        # Crear producto
        producto = Producto(
            tipo_producto='simple',
            id_articulo=articulo.id,
            id_precio_compra=id_precio_compra,
            id_color=id_color,
            id_proveedor=id_proveedor
        )
        self.db.add(producto)
        self.db.flush()
        
        # Crear producto simple
        producto_simple = ProductoSimple(
            articulo=articulo,
            especificaciones=None,   
        )
        self.db.add(producto_simple)
        self.db.flush()
        
        # Crear stock inicial
        stock = Stock(
            id_producto_simple=producto_simple.id,
            cantidad_actual=0,
            cantidad_minima=5
        )
        self.db.add(stock)
        
        self.db.commit()
        
        return {
            'articulo': articulo,
            'producto': producto,
            'producto_simple': producto_simple,
            'stock': stock
        }
    
    def crear_pack_completo(
        self,
        nombre_pack: str,
        id_familia: int,
        precio_venta: float,
        productos_ids: List[Dict[str, Any]],  # [{'id': 1, 'cantidad': 2}, ...]
        descripcion_pack: Optional[str] = None,
        descuento_porcentaje: Optional[int] = None,
        sku: Optional[str] = None
    ) -> Dict[str, Any]:
        """Crea un pack completo con sus productos asociados"""
        
        # Crear precio de venta
        precio_v = PrecioVenta(precio=precio_venta)
        self.db.add(precio_v)
        self.db.flush()
        
        # Crear artículo
        articulo = Articulo(
            nombre=nombre_pack,
            descripcion=descripcion_pack,
            sku=sku,
            id_familia=id_familia,
            id_precio_venta=precio_v.id
        )
        self.db.add(articulo)
        self.db.flush()
        
        # Crear pack
        pack = Pack(
            nombre_pack=nombre_pack,
            descripcion_pack=descripcion_pack,
            descuento_porcentaje=descuento_porcentaje,
            id_articulo=articulo.id
        )
        self.db.add(pack)
        self.db.flush()
        
        # Asociar productos al pack
        pack_productos = []
        for prod_data in productos_ids:
            pack_producto = PackProducto(
                id_pack=pack.id,
                id_producto=prod_data['id'],
                cantidad_incluida=prod_data.get('cantidad', 1)
            )
            self.db.add(pack_producto)
            pack_productos.append(pack_producto)
        
        self.db.commit()
        
        return {
            'articulo': articulo,
            'pack': pack,
            'pack_productos': pack_productos
        }
    
    def obtener_stock_bajo_minimo(self) -> List[Stock]:
        """Obtiene todos los elementos con stock por debajo del mínimo"""
        return self.db.query(Stock).filter(
            Stock.necesita_reposicion == True
        ).all()
    
    def calcular_precio_producto_compuesto(self, id_producto_compuesto: int) -> float:
        """Calcula el precio de un producto compuesto basado en sus componentes"""
        producto_compuesto = self.db.query(ProductoCompuesto).filter(
            ProductoCompuesto.id == id_producto_compuesto
        ).first()
        
        if not producto_compuesto:
            return 0.0
        
        precio_total = 0.0
        for cp in producto_compuesto.componente_productos:
            if cp.componente.precio_compra:
                precio_total += float(cp.componente.precio_compra.precio) * float(cp.cantidad_necesaria)
        
        return precio_total
    
    def verificar_stock_suficiente_producto_compuesto(self, id_producto_compuesto: int, cantidad_deseada: int = 1) -> Dict[str, Any]:
        """Verifica si hay stock suficiente para fabricar un producto compuesto"""
        producto_compuesto = self.db.query(ProductoCompuesto).filter(
            ProductoCompuesto.id == id_producto_compuesto
        ).first()
        
        if not producto_compuesto:
            return {'puede_fabricar': False, 'faltantes': []}
        
        faltantes = []
        puede_fabricar = True
        
        for cp in producto_compuesto.componente_productos:
            cantidad_necesaria = float(cp.cantidad_necesaria) * cantidad_deseada
            if cp.componente.stock:
                stock_disponible = float(cp.componente.stock.cantidad_actual)
                if stock_disponible < cantidad_necesaria:
                    puede_fabricar = False
                    faltantes.append({
                        'componente': cp.componente.nombre,
                        'necesario': cantidad_necesaria,
                        'disponible': stock_disponible,
                        'faltante': cantidad_necesaria - stock_disponible
                    })
        
        return {
            'puede_fabricar': puede_fabricar,
            'faltantes': faltantes
        }
