"""
🎨 Rutas para el modelo Color

Endpoints RESTful para gestionar los colores de productos.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
from app.schemas.colorDTO import ColorCreate, ColorResponse, ColorUpdate
from app.services.color_service import ColorService

router = APIRouter(prefix="/colores", tags=["Colores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# ENDPOINTS CRUD BÁSICOS
# ==========================================

@router.get("/", response_model=List[ColorResponse], responses={
    200: {"description": "Lista de colores obtenida exitosamente"},
    500: {"description": "Error interno del servidor"}
})
def listar_colores(
    offset: int = 0,
    limite: int = 100,
    db: Session = Depends(get_db)
):
    """
    📋 Obtener lista de colores con filtros opcionales
    """
    try:
        color_service = ColorService(db)
        colores = color_service.obtener_todos(
            offset=offset,
            limite=limite
        )
        return colores
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar colores: {str(e)}"
        )

@router.get("/{color_id}", response_model=ColorResponse, responses={
    200: {"description": "Color encontrado exitosamente"},
    404: {"description": "Color no encontrado"},
    500: {"description": "Error interno del servidor"}
    })
def obtener_color(
    color_id: int,
    db: Session = Depends(get_db)
):
    """
    🔍 Obtener un color específico por ID
    """
    try:
        color_service = ColorService(db)
        color = color_service.obtener_por_id(color_id)
        if not color:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Color no encontrado"
            )
        return color
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener color: {str(e)}"
        )

@router.post("/", response_model=ColorResponse, status_code=status.HTTP_201_CREATED, responses={
    201: {"description": "Color creado exitosamente"},
    400: {"description": "Error de validación de datos"},
    500: {"description": "Error interno del servidor"}
    })
def crear_color(
    color: ColorCreate,
    db: Session = Depends(get_db)
):
    """
    🆕 Crear un nuevo color
    """
    try:
        color_service = ColorService(db)
        return color_service.crear_color(color)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear color: {str(e)}"
        )

@router.put("/{color_id}", response_model=ColorResponse, responses={
    200: {"description": "Color actualizado exitosamente"},
    404: {"description": "Color no encontrado"},
    400: {"description": "Error de validación de datos"},
    500: {"description": "Error interno del servidor"}
    })
def actualizar_color(
    color_id: int,
    color: ColorUpdate,
    db: Session = Depends(get_db)
):
    """
    ✏️ Actualizar un color existente
    """
    try:
        color_service = ColorService(db)
        color_actualizado = color_service.actualizar_color(color_id, color)
        if not color:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Color no encontrado"
            )
        return color_actualizado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar color: {str(e)}"
        )

@router.delete("/{color_id}", response_model=dict, responses={
    200: {"description": "Color eliminado exitosamente"},
    400: {"description": "Error al eliminar color"},
    404: {"description": "Color no encontrado"},
    500: {"description": "Error interno del servidor"}
    })
def eliminar_color(
    color_id: int,
    db: Session = Depends(get_db)
):
    """
    🗑️ Eliminar un color (soft delete)
    """
    try:
        color_service = ColorService(db)
        # Validar si el color existe antes de eliminar
        if not color_service.obtener_por_id(color_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Color no encontrado"
            )
        # Validar si se puede eliminar
        success = color_service.validar_eliminacion(color_id)

        if not success['puede_eliminar']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error validando eliminación del color {color_id}:\n\tRazón: {success['razon']}\n\tElementos relacionados: {success['elementos_relacionados']}"
            )
        else:
            success = color_service.eliminar(color_id)
        return {"detail": "Color eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar color: {str(e)}"
        )
