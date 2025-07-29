"""
🚀 FastAPI Application - Sistema de Inventario Oficit

Aplicación principal que coordina todos los endpoints del sistema de inventario.
Organizada por modelos con rutas específicas para cada entidad.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal

# Importar todos los routers de rutas
from app.routes import (
    familia_router,
    color_router,
    proveedor_router,
    precio_router,
    articulo_router,
    componente_router,
    producto_router,
    pack_router,
    stock_router,
    inventario_router
)

# Configuración de la aplicación
app = FastAPI(
    title="🏢 Oficit Stock Service",
    description="""
    ## Sistema de Inventario Completo
    
    API RESTful para gestión integral de inventario con:
    - 👥 **Familias y Colores**: Organización por categorías
    - 🏢 **Proveedores**: Gestión de proveedores y contactos  
    - 💰 **Precios**: Control de precios de compra y venta
    - 📦 **Artículos**: Catálogo base de productos
    - 🔧 **Componentes**: Elementos para productos compuestos
    - 🏷️ **Productos**: Simples y compuestos
    - 📊 **Stock**: Control de inventario y movimientos
    - 🎯 **Coordinador**: Operaciones complejas del inventario
    
    ### Características:
    - ✅ CRUD completo para todas las entidades
    - ✅ Relaciones complejas entre modelos
    - ✅ Validaciones de integridad
    - ✅ Reportes y análisis avanzados
    - ✅ Sistema de alertas de stock
    """,
    version="2.0.0",
    contact={
        "name": "Equipo Oficit",
        "email": "tech@oficit.com",
    },
    license_info={
        "name": "MIT License",
    },
)

def get_db():
    """
    🔌 Dependencia para obtener sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# ENDPOINT RAÍZ
# ==========================================

@app.get("/", tags=["Sistema"])
def read_root():
    """
    🏠 Endpoint raíz - Estado del servicio
    """
    return {
        "servicio": "Oficit Stock Service",
        "version": "2.0.0",
        "estado": "✅ Activo",
        "mensaje": "Sistema de inventario funcionando correctamente",
        "documentacion": "/docs",
        "endpoints_disponibles": {
            "familias": "/familias",
            "colores": "/colores", 
            "proveedores": "/proveedores",
            "precios": "/precios",
            "articulos": "/articulos",
            "componentes": "/componentes",
            "productos": "/productos",
            "packs": "/packs",
            "stock": "/stock",
            "inventario": "/inventario"
        }
    }

@app.get("/health", tags=["Sistema"])
def health_check(db: Session = Depends(get_db)):
    """
    🏥 Verificación de salud del sistema
    """
    try:
        # Verificar conexión a base de datos
        db.execute("SELECT 1")
        return {
            "estado": "✅ Saludable",
            "base_datos": "✅ Conectada",
            "timestamp": "2025-07-29T00:00:00Z"
        }
    except Exception as e:
        return {
            "estado": "❌ Error",
            "base_datos": "❌ Desconectada",
            "error": str(e),
            "timestamp": "2025-07-29T00:00:00Z"
        }

# ==========================================
# REGISTRO DE ROUTERS POR MODELO
# ==========================================

# Modelos base (sin dependencias fuertes)
app.include_router(familia_router)
app.include_router(color_router)
app.include_router(proveedor_router)
app.include_router(precio_router)

# Modelos intermedios (dependen de los base)
app.include_router(articulo_router)
app.include_router(componente_router)

# Modelos complejos (dependen de intermedios)  
app.include_router(producto_router)
app.include_router(pack_router)
app.include_router(stock_router)

# Servicio coordinador (operaciones complejas)
app.include_router(inventario_router)

# ==========================================
# CONFIGURACIÓN ADICIONAL
# ==========================================

# Middleware para CORS (si es necesario)
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
