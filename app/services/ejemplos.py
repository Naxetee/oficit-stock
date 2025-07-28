"""
🎯 Ejemplo de Uso de la Arquitectura de Servicios

Este archivo muestra ejemplos prácticos de cómo usar los servicios
individuales y el servicio coordinador principal InventarioService.
"""

from sqlalchemy.orm import Session
from app.services import (
    FamiliaService, ColorService, ProveedorService, PrecioService,
    ArticuloService, ProductoService, ComponenteService, PackService,
    StockService, InventarioService
)

def ejemplo_uso_servicios_individuales(db_session: Session):
    """
    Ejemplo de uso de servicios individuales para operaciones específicas
    """
    print("🚀 Ejemplo de uso de servicios individuales\n")
    
    try:
        # 1. Crear una familia de productos
        familia_service = FamiliaService(db_session)
        familia = familia_service.crear_familia(
            nombre="Electrónicos",
            descripcion="Productos electrónicos diversos"
        )
        print(f"✅ Familia creada: {familia.nombre} (ID: {familia.id})")
    except Exception as e:
        print(f"❌ Error creando familia: {e}")
        pass
    
    try:
        # 2. Crear un color
        color_service = ColorService(db_session)
        color = color_service.crear_color(
            nombre="Negro",
            codigo_hex="#000000"
        )
        print(f"✅ Color creado: {color.nombre} (ID: {color.id})")
    except Exception as e:
        print(f"❌ Error creando color: {e}")
        pass
    
    try:
        # 3. Crear un proveedor
        proveedor_service = ProveedorService(db_session)
        proveedor = proveedor_service.crear_proveedor(
            nombre="TechSupplier S.L.",
            nif_cif="B12345678",
            email="contacto@techsupplier.es",
            telefono="912345678"
        )
        print(f"✅ Proveedor creado: {proveedor.nombre} (ID: {proveedor.id})")
    except Exception as e:
        print(f"❌ Error creando proveedor: {e}")
        pass

    try:
        # 4. Crear precios
        precio_service = PrecioService(db_session)
        precio_compra = precio_service.crear_precio_compra(50.0)
        precio_venta = precio_service.crear_precio_venta(80.0)
        print(f"✅ Precios creados - Compra: €{precio_compra.valor}, Venta: €{precio_venta.valor}")
    except Exception as e:
        print(f"❌ Error creando precios: {e}")
        pass
    
    try:
        # 5. Crear artículo
        articulo_service = ArticuloService(db_session)
        articulo = articulo_service.crear_articulo(
            nombre="Smartphone XYZ",
            descripcion="Smartphone última generación",
            codigo="PHONE001",
            id_familia=familia.id,
            id_precio_venta=precio_venta.id
        )
        print(f"✅ Artículo creado: {articulo.nombre} (ID: {articulo.id})")
    except Exception as e:
        print(f"❌ Error creando artículo: {e}")
        pass

    try:
        # 6. Crear producto simple
        producto_service = ProductoService(db_session)
        producto_data = producto_service.crear_producto_simple_completo(
            id_articulo=articulo.id,
            especificaciones="128GB, 6GB RAM",
            id_proveedor=proveedor.id,
            id_precio_compra=precio_compra.id,
            id_color=color.id
        )
        print(f"✅ Producto simple creado: {producto_data['producto'].id}")
    except Exception as e:
        print(f"❌ Error creando producto simple: {e}")
        pass

    try:
        # 7. Crear stock
        stock_service = StockService(db_session)
        # Comprobar si existe el stock del producto
        stock = stock_service.obtener_stock_por_producto(producto_data['producto'].id)
        stock_service.crear_movimiento_stock(
            stock_id=stock.id if stock else None,
            cantidad=100,
            tipo_movimiento='entrada',
            motivo="Stock inicial"
        )
        print(f"✅ Stock creado con 100 unidades")
    except Exception as e:
        print(f"❌ Error creando stock: {e}")
        pass

    print("\n🎯 Servicios individuales completados exitosamente!\n")


def ejemplo_uso_servicio_coordinador(db_session: Session):
    """
    Ejemplo de uso del servicio coordinador para operaciones complejas
    """
    print("🎯 Ejemplo de uso del Servicio Coordinador (InventarioService)\n")
    
    inventario = InventarioService(db_session)
    
    # 1. Crear producto simple completo en una sola operación
    producto_simple = inventario.crear_producto_simple_completo(
        nombre_articulo="Auriculares Bluetooth",
        descripcion_articulo="Auriculares inalámbricos con cancelación de ruido",
        codigo_articulo="AUR001",
        precio_venta=45.99,
        precio_compra=25.00,
        especificaciones="Bluetooth 5.0, Cancelación activa de ruido",
        stock_inicial=50,
        stock_minimo=10,
        ubicacion_almacen="Almacén B2",
        familia_id=1,  # Asumiendo que la familia ya existe
        proveedor_id=1,  # Asumiendo que el proveedor ya existe
    )
    print(f"✅ Producto simple completo creado: {producto_simple['articulo'].nombre}")
    
    # 2. Crear producto compuesto con componentes
    # Primero necesitamos algunos componentes
    comp1 = inventario.crear_producto_simple_completo(
        nombre_articulo="Placa Base",
        codigo_articulo="PCB001",
        precio_compra=80.0,
        stock_inicial=20,
        stock_minimo=5
    )
    
    comp2 = inventario.crear_producto_simple_completo(
        nombre_articulo="Procesador",
        codigo_articulo="CPU001", 
        precio_compra=150.0,
        stock_inicial=15,
        stock_minimo=3
    )
    
    # Ahora crear el producto compuesto
    producto_compuesto = inventario.crear_producto_compuesto_completo(
        nombre_articulo="PC Gaming Custom",
        descripcion_articulo="PC Gaming personalizado",
        codigo_articulo="PC001",
        precio_venta=450.0,
        descripcion_compuesto="PC Gaming de alto rendimiento",
        componentes_necesarios=[
            {'id_componente': comp1['componente'].id, 'cantidad_necesaria': 1},
            {'id_componente': comp2['componente'].id, 'cantidad_necesaria': 1}
        ]
    )
    print(f"✅ Producto compuesto creado: {producto_compuesto['articulo'].nombre}")
    
    # 3. Crear pack completo
    pack = inventario.crear_pack_completo(
        nombre_pack="Pack Gamer Completo",
        descripcion_articulo="Pack completo para gaming",
        codigo_articulo="PACK001",
        precio_venta=550.0,
        descripcion_pack="Todo lo necesario para gaming",
        descuento_porcentaje=10,
        productos_incluidos=[
            {'id_producto': producto_simple['producto'].id, 'cantidad': 1},
            {'id_producto': producto_compuesto['producto'].id, 'cantidad': 1}
        ]
    )
    print(f"✅ Pack completo creado: {pack['articulo'].nombre}")
    
    # 4. Obtener dashboard del inventario
    dashboard = inventario.obtener_dashboard_inventario()
    print(f"\n📊 Dashboard del Inventario:")
    print(f"   • Total artículos: {dashboard['total_articulos']}")
    print(f"   • Total productos: {dashboard['total_productos']}")
    print(f"   • Productos simples: {dashboard['productos_simples']}")
    print(f"   • Productos compuestos: {dashboard['productos_compuestos']}")
    print(f"   • Total componentes: {dashboard['total_componentes']}")
    print(f"   • Total packs: {dashboard['total_packs']}")
    print(f"   • Total proveedores: {dashboard['total_proveedores']}")
    print(f"   • Alertas de reposición: {dashboard['alertas_reposicion']}")
    
    # 5. Búsqueda global
    resultados = inventario.buscar_elementos_inventario("Gaming")
    print(f"\n🔍 Búsqueda 'Gaming':")
    print(f"   • Artículos encontrados: {len(resultados['articulos'])}")
    print(f"   • Componentes encontrados: {len(resultados['componentes'])}")
    
    print("\n🎯 Servicio coordinador completado exitosamente!")


def ejemplo_operaciones_avanzadas(db_session: Session):
    """
    Ejemplo de operaciones más avanzadas usando la combinación de servicios
    """
    print("🔥 Ejemplo de operaciones avanzadas\n")
    
    inventario = InventarioService(db_session)
    
    # 1. Análisis de stock bajo mínimo
    stock_bajo = inventario.stock_service.obtener_stock_bajo_minimo()
    if stock_bajo:
        print(f"⚠️  {len(stock_bajo)} productos con stock bajo el mínimo:")
        for stock in stock_bajo[:3]:  # Mostrar solo los primeros 3
            print(f"   • {stock.producto_simple.articulo.nombre}: {stock.cantidad_actual}/{stock.cantidad_minima}")
    
    # 2. Obtener productos de un proveedor específico
    proveedores = inventario.proveedor_service.obtener_todos()
    if proveedores:
        proveedor = proveedores[0]
        productos_proveedor = inventario.proveedor_service.obtener_productos_por_proveedor(proveedor.id)
        print(f"\n📦 Productos del proveedor '{proveedor.nombre}': {len(productos_proveedor)}")
    
    # 3. Análisis de precios
    precios_venta = inventario.precio_service.obtener_precios_venta_activos()
    if precios_venta:
        precio_promedio = sum(p.valor for p in precios_venta) / len(precios_venta)
        precio_max = max(p.valor for p in precios_venta)
        precio_min = min(p.valor for p in precios_venta)
        
        print(f"\n💰 Análisis de precios de venta:")
        print(f"   • Precio promedio: €{precio_promedio:.2f}")
        print(f"   • Precio máximo: €{precio_max:.2f}")
        print(f"   • Precio mínimo: €{precio_min:.2f}")
    
    # 4. Gestión de familias y sus estadísticas
    familias = inventario.familia_service.obtener_familias_con_estadisticas()
    print(f"\n👥 Estadísticas por familia:")
    for familia_stats in familias[:3]:  # Mostrar solo las primeras 3
        print(f"   • {familia_stats['familia'].nombre}: {familia_stats['total_articulos']} artículos")
    
    print("\n🔥 Operaciones avanzadas completadas!")


if __name__ == "__main__":
    # Este código se ejecutaría si tienes una sesión de base de datos configurada
    print("🎯 Ejemplos de Uso de la Arquitectura de Servicios")
    print("=" * 60)
    print()
    print("Para usar estos ejemplos, necesitas:")
    print("1. Una sesión de SQLAlchemy configurada")
    print("2. Las tablas de la base de datos creadas")
    print("3. Importar este módulo y llamar a las funciones con tu sesión")
    print()
    print("Ejemplo de uso:")
    print("from sqlalchemy.orm import sessionmaker")
    print("from app.db import SessionLocal")
    print("from app.services.ejemplos import ejemplo_uso_servicio_coordinador")
    print()
    print("with SessionLocal() as session:")
    print("    ejemplo_uso_servicio_coordinador(session)")
