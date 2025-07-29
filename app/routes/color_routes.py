"""
🎨 Rutas para el modelo Color

Endpoints RESTful para gestionar los colores de productos.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
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

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_color(
    nombre: str,
    codigo_hex: Optional[str] = None,
    url_imagen: Optional[str] = None,
    id_familia: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    🆕 Crear un nuevo color
    """
    try:
        color_service = ColorService(db)
        color = color_service.crear_color(
            nombre=nombre,
            codigo_hex=codigo_hex,
            url_imagen=url_imagen,
            id_familia=id_familia
        )
        return {
            "mensaje": "Color creado exitosamente",
            "color": {
                "id": color.id,
                "nombre": color.nombre,
                "codigo_hex": color.codigo_hex,
                "url_imagen": color.url_imagen,
                "id_familia": color.id_familia
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear color: {str(e)}"
        )

@router.get("/", response_model=List[dict])
def listar_colores(
    activo: Optional[bool] = None,
    id_familia: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    📋 Obtener lista de colores con filtros opcionales
    """
    try:
        color_service = ColorService(db)
        colores = color_service.listar_colores(
            activo=activo,
            id_familia=id_familia,
            skip=skip,
            limit=limit
        )
        return [
            {
                "id": color.id,
                "nombre": color.nombre,
                "codigo_hex": color.codigo_hex,
                "url_imagen": color.url_imagen,
                "activo": color.activo,
                "id_familia": color.id_familia,
                "created_at": color.created_at,
                "updated_at": color.updated_at
            }
            for color in colores
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar colores: {str(e)}"
        )

@router.get("/{color_id}", response_model=dict)
def obtener_color(
    color_id: int,
    db: Session = Depends(get_db)
):
    """
    🔍 Obtener un color específico por ID
    """
    try:
        color_service = ColorService(db)
        color = color_service.obtener_color(color_id)
        if not color:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Color no encontrado"
            )
        return {
            "id": color.id,
            "nombre": color.nombre,
            "codigo_hex": color.codigo_hex,
            "url_imagen": color.url_imagen,
            "activo": color.activo,
            "id_familia": color.id_familia,
            "created_at": color.created_at,
            "updated_at": color.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener color: {str(e)}"
        )

@router.put("/{color_id}", response_model=dict)
def actualizar_color(
    color_id: int,
    nombre: Optional[str] = None,
    codigo_hex: Optional[str] = None,
    url_imagen: Optional[str] = None,
    activo: Optional[bool] = None,
    id_familia: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    ✏️ Actualizar un color existente
    """
    try:
        color_service = ColorService(db)
        color = color_service.actualizar_color(
            color_id=color_id,
            nombre=nombre,
            codigo_hex=codigo_hex,
            url_imagen=url_imagen,
            activo=activo,
            id_familia=id_familia
        )
        if not color:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Color no encontrado"
            )
        return {
            "mensaje": "Color actualizado exitosamente",
            "color": {
                "id": color.id,
                "nombre": color.nombre,
                "codigo_hex": color.codigo_hex,
                "url_imagen": color.url_imagen,
                "activo": color.activo,
                "id_familia": color.id_familia
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar color: {str(e)}"
        )

@router.delete("/{color_id}", response_model=dict)
def eliminar_color(
    color_id: int,
    db: Session = Depends(get_db)
):
    """
    🗑️ Eliminar un color (soft delete)
    """
    try:
        color_service = ColorService(db)
        success = color_service.eliminar_color(color_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Color no encontrado"
            )
        return {"mensaje": "Color eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar color: {str(e)}"
        )
