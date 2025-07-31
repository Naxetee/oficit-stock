"""
🎯 Rutas para el Servicio Coordinador de Inventario

Endpoints RESTful para operaciones complejas que coordinan múltiples modelos.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.db import SessionLocal
from app.services.inventario_service import InventarioService

router = APIRouter(prefix="/inventario", tags=["Inventario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# ENDPOINTS DE CONFIGURACIÓN INICIAL
# ==========================================

@router.post("/setup/completo", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_setup_completo(
    datos_setup: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """🚀 Crear un setup completo del inventario con todos los elementos relacionados"""
    try:
        inventario_service = InventarioService(db)
        resultado = inventario_service.crear_setup_completo(datos_setup)
        return {
            "mensaje": "Setup completo creado exitosamente",
            "elementos_creados": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error en setup completo: {str(e)}")

# ==========================================
# ENDPOINTS DE ANÁLISIS Y REPORTES
# ==========================================

@router.get("/dashboard", response_model=dict)
def obtener_dashboard(db: Session = Depends(get_db)):
    """📊 Obtener datos del dashboard principal"""
    try:
        inventario_service = InventarioService(db)
        dashboard = inventario_service.obtener_dashboard()
        return dashboard
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener dashboard: {str(e)}")

@router.get("/resumen/general", response_model=dict)
def obtener_resumen_general(db: Session = Depends(get_db)):
    """📈 Obtener resumen general del inventario"""
    try:
        inventario_service = InventarioService(db)
        resumen = inventario_service.obtener_resumen_general()
        return resumen
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener resumen: {str(e)}")

@router.get("/alertas", response_model=dict)
def obtener_alertas_inventario(db: Session = Depends(get_db)):
    """⚠️ Obtener todas las alertas del inventario"""
    try:
        inventario_service = InventarioService(db)
        alertas = inventario_service.obtener_alertas_generales()
        return alertas
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener alertas: {str(e)}")

# ==========================================
# ENDPOINTS DE OPERACIONES COMPLEJAS
# ==========================================

@router.post("/producto/completo", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_producto_completo(
    datos_producto: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """🏷️ Crear un producto completo con todos sus elementos relacionados"""
    try:
        inventario_service = InventarioService(db)
        producto = inventario_service.crear_producto_completo(datos_producto)
        return {
            "mensaje": "Producto completo creado exitosamente",
            "producto": {
                "id": producto.id,
                "tipo_producto": producto.tipo_producto,
                "id_articulo": producto.id_articulo
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear producto completo: {str(e)}")

@router.post("/pack/completo", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_pack_completo(
    datos_pack: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """📦 Crear un pack completo con productos incluidos"""
    try:
        inventario_service = InventarioService(db)
        pack = inventario_service.crear_pack_completo(datos_pack)
        return {
            "mensaje": "Pack completo creado exitosamente",
            "pack": {
                "id": pack.id,
                "nombre": pack.nombre,
                "id_articulo": pack.id_articulo
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear pack completo: {str(e)}")

# ==========================================
# ENDPOINTS DE CONSULTAS AVANZADAS
# ==========================================

@router.get("/buscar/avanzada", response_model=List[dict])
def busqueda_avanzada(
    termino: str,
    tipo_busqueda: Optional[str] = "todo",  # "producto", "componente", "articulo", "todo"
    filtros: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db)
):
    """🔍 Búsqueda avanzada en el inventario"""
    try:
        inventario_service = InventarioService(db)
        resultados = inventario_service.busqueda_avanzada(termino, tipo_busqueda, filtros or {})
        return resultados
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en búsqueda avanzada: {str(e)}")

@router.get("/analisis/costos", response_model=dict)
def analisis_costos(
    id_producto: Optional[int] = None,
    id_familia: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """💰 Análisis de costos de productos o familias"""
    try:
        inventario_service = InventarioService(db)
        analisis = inventario_service.analizar_costos(id_producto, id_familia)
        return analisis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en análisis de costos: {str(e)}")

@router.get("/reporte/valoracion", response_model=dict)
def reporte_valoracion_inventario(
    fecha_corte: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """📊 Reporte de valoración del inventario"""
    try:
        inventario_service = InventarioService(db)
        reporte = inventario_service.generar_reporte_valoracion(fecha_corte)
        return reporte
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al generar reporte: {str(e)}")

# ==========================================
# ENDPOINTS DE VALIDACIÓN Y MANTENIMIENTO
# ==========================================

@router.get("/validacion/integridad", response_model=dict)
def validar_integridad_datos(db: Session = Depends(get_db)):
    """🔧 Validar integridad de datos del inventario"""
    try:
        inventario_service = InventarioService(db)
        validacion = inventario_service.validar_integridad_datos()
        return validacion
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en validación: {str(e)}")

@router.post("/mantenimiento/limpiar-huerfanos", response_model=dict)
def limpiar_registros_huerfanos(db: Session = Depends(get_db)):
    """🧹 Limpiar registros huérfanos del inventario"""
    try:
        inventario_service = InventarioService(db)
        resultado = inventario_service.limpiar_registros_huerfanos()
        return {
            "mensaje": "Limpieza de registros huérfanos completada",
            "registros_eliminados": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error en limpieza: {str(e)}")

@router.get("/exportar/{formato}", response_model=dict)
def exportar_inventario(
    formato: str,  # "csv", "excel", "json"
    incluir_stock: bool = True,
    db: Session = Depends(get_db)
):
    """📤 Exportar inventario en diferentes formatos"""
    try:
        if formato not in ["csv", "excel", "json"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato no válido")
        
        inventario_service = InventarioService(db)
        resultado = inventario_service.exportar_inventario(formato, incluir_stock)
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al exportar: {str(e)}")
