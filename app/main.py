"""
🚀 FastAPI Application - Sistema de Inventario Oficit

Aplicación principal que coordina todos los endpoints del sistema de inventario.
Organizada por modelos con rutas específicas para cada entidad.
"""

from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
from dotenv import load_dotenv
import os

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import engine
from fastapi.staticfiles import StaticFiles
from starlette.authentication import (
    AuthenticationBackend
)
from starlette.middleware.sessions import SessionMiddleware

# Importar todos los routers de rutas
from app.routes.articulo_router import router as articulo_router
from app.routes.stock_router import router as stock_router
from app.routes.familia_router import router as familia_router
from app.routes.proveedor_router import router as proveedor_router
from app.routes.color_router import router as color_router
from app.routes.componente_router import router as componente_router
from app.admin.sqladmin_setup import CustomAdmin, register_admin_views

# Importar la función get_db para inyección de dependencias
from app.db import get_db

# Configuración de la aplicación
app = FastAPI(
    title="🏢 Oficit Stock Service",
    description="""
    ## Sistema de Inventario Completo

    API RESTful para gestión integral de inventario con:
    - 👥 Familias y Colores: Organización por categorías
    - 🏢 Proveedores: Gestión de proveedores y contactos  
    - 📦 Artículos: Catálogo base de productos (simples, compuestos y packs)
    - 🔧 Componentes: Elementos para productos compuestos
    - 🏷️ Productos: Simples y compuestos
    - 📊 Stock: Control de inventario y movimientos
    - 🎯 Coordinador: Operaciones complejas del inventario
    - 🛠️ Panel de administración SQLAdmin en `/admin`

    ### Características:
    - ✅ CRUD completo para todas las entidades
    - ✅ Relaciones complejas entre modelos
    - ✅ Validaciones de integridad
    - ✅ Reportes y análisis avanzados
    - ✅ Sistema de alertas de stock
    - ✅ Panel de administración visual SQLAdmin

    ---
    ## 🔒 Licencia y uso

    > ⚠️ Este software es propiedad de Tienda Oficit SL. Queda prohibida su copia, distribución o uso fuera de la empresa sin autorización expresa.
    """,
    version="1.0.0",
    contact={
        "name": "Tienda Oficit SLU",
    },
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Añade soporte de sesiones
app.add_middleware(SessionMiddleware, secret_key="oficit-secret-key")

# Montar la carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="app/admin/static"), name="static")

# ==========================================
# AUTENTICACIÓN PARA ADMIN
# ==========================================
from sqladmin.authentication import AuthenticationBackend

load_dotenv()
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

class OficitAuthBackend(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)

    async def authenticate(self, request):
        user = request.session.get("user")
        if user:
            return user
        return None

    async def login(self, request):
        if request.method == "GET":
            error = request.query_params.get("error")
            return HTMLResponse(f"""
            <html>
                <head>
                    <title>Login Oficit</title>
                    <link rel="stylesheet" href="/static/custom.css">
                </head>
                <body style="background:#f5f6fa;">
                    <div style="max-width:400px;margin:80px auto;padding:2em;background:white;border-radius:8px;box-shadow:0 2px 8px #0001;">
                        <h2>Iniciar sesión</h2>
                        {f'<div style="color:red;">{error}</div>' if error else ''}
                        <form method="post">
                            <input name="username" placeholder="Usuario" style="width:100%;margin-bottom:1em;padding:0.5em;">
                            <input name="password" type="password" placeholder="Contraseña" style="width:100%;margin-bottom:1em;padding:0.5em;">
                            <button type="submit" style="width:100%;padding:0.5em;background:#0e7490;color:white;border:none;">Entrar</button>
                        </form>
                    </div>
                </body>
            </html>
            """)
        else:
            form = await request.form()
            username = form.get("username")
            password = form.get("password")
            if username == ADMIN_USER and password == ADMIN_PASSWORD:
                request.session["user"] = username
                return RedirectResponse(url="/admin", status_code=302)
            return RedirectResponse(url="/admin/login?error=Credenciales+incorrectas", status_code=302)

    async def logout(self, request):
        request.session.clear()
        return RedirectResponse(url="/admin/login", status_code=302)

# ==========================================
# SQLAdmin Panel
# ==========================================
admin = CustomAdmin(
    app,
    engine,
    base_url="/admin",
    authentication_backend=OficitAuthBackend(secret_key="oficit-secret-key"),
)


# Importa y registra las vistas de SQLAdmin
register_admin_views(admin)

# ====

# Favicon handler para evitar 404 de navegadores
from fastapi.responses import FileResponse

@app.get("/favicon.ico")
def favicon():
    return FileResponse("app/admin/static/favicon.ico")

# ENDPOINT RAÍZ
# ====

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
            "familia": "/familia",
            "color": "/color",
            "proveedor": "/proveedor",
            "componente": "/componente",
            "articulo": "/articulo"
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
app.include_router(articulo_router)
app.include_router(proveedor_router)
app.include_router(color_router)
app.include_router(componente_router)
app.include_router(stock_router)

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