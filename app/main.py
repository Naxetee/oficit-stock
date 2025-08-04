"""
🚀 FastAPI Application - Sistema de Inventario Oficit

Aplicación principal que coordina todos los endpoints del sistema de inventario.
Organizada por modelos con rutas específicas para cada entidad.
"""

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import SessionLocal

# Importar todos los routers de rutas
from app.routes.familia_router import router as familia_router
from app.routes.pack_router import router as pack_router
from app.routes.proveedor_router import router as proveedor_router
from app.routes.producto_simple_router import router as producto_simple_router
from app.routes.producto_compuesto_router import router as producto_compuesto_router
from app.routes.color_router import router as color_router
from app.routes.componente_router import router as componente_router

# Configuración de la aplicación
app = FastAPI(
    title="🏢 Oficit Stock Service",
    description="""
    ## Sistema de Inventario Completo

    API RESTful para gestión integral de inventario con:
    - 👥 Familias y Colores: Organización por categorías
    - 🏢 Proveedores: Gestión de proveedores y contactos  
    - 📦 Artículos: Catálogo base de productos
    - 🔧 Componentes: Elementos para productos compuestos
    - 🏷️ Productos: Simples y compuestos
    - 📊 Stock: Control de inventario y movimientos
    - 🎯 Coordinador: Operaciones complejas del inventario

    ### Características:
    - ✅ CRUD completo para todas las entidades
    - ✅ Relaciones complejas entre modelos
    - ✅ Validaciones de integridad
    - ✅ Reportes y análisis avanzados
    - ✅ Sistema de alertas de stock

    ---
    ## 🔒 Licencia y uso

    > ⚠️ Este software es propiedad de Tienda Oficit SL. Queda prohibida su copia, distribución o uso fuera de la empresa sin autorización expresa.
    """,
    version="1.0.0",
    contact={
        "name": "Tienda Oficit SLU",
    },
    # Ocultar 422 globalmente
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Datos inválidos en la petición"}
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
        "version": "1.0.0",
        "estado": "✅ Activo",
        "mensaje": "Sistema de inventario funcionando correctamente",
        "documentacion": app.docs_url,
        "estado_del_sistema": "/health",
        "endpoints_disponibles": {
            "familias": "/familia",
            "colores": "/color",
            "proveedores": "/proveedor",
            "productos_simples": "/producto-simple",
            "productos_compuestos": "/producto-compuesto",
            "componentes": "/componente",
            "packs": "/packs"
        }
    }

@app.get("/health", tags=["Sistema"])
def health_check(db: Session = Depends(get_db)):
    """
    🏥 Verificación de salud del sistema
    """
    try:
        # Verificar conexión a base de datos
        q = text('SELECT 1')  # SQL estándar para verificar conexión
        db.execute(q)
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

app.include_router(familia_router)
app.include_router(pack_router)
app.include_router(proveedor_router)
app.include_router(producto_simple_router)
app.include_router(producto_compuesto_router)
app.include_router(color_router)
app.include_router(componente_router)

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
    uvicorn.run(
        "app.main:app", 
        host="localhost", 
        port=8000, 
        reload=True,
        log_level="info"
    )
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )