"""
🏷️ Rutas para el modelo Familia

Endpoints RESTful para gestionar las familias de productos.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
from app.services.familia_service import FamiliaService
from app.models.familia import Familia

router = APIRouter(prefix="/familias", tags=["Familias"])

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
def crear_familia(
    nombre: str,
    descripcion: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    🆕 Crear una nueva familia de productos
    """
    try:
        familia_service = FamiliaService(db)
        familia = familia_service.crear_familia(nombre=nombre, descripcion=descripcion)
        return {
            "mensaje": "Familia creada exitosamente",
            "familia": {
                "id": familia.id,
                "nombre": familia.nombre,
                "descripcion": familia.descripcion
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear familia: {str(e)}"
        )

@router.get("/", response_model=List[dict])
def listar_familias(
    activo: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    📋 Obtener lista de familias con filtros opcionales
    """
    try:
        familia_service = FamiliaService(db)
        familias = familia_service.listar_familias(
            activo=activo, 
            skip=skip, 
            limit=limit
        )
        return [
            {
                "id": familia.id,
                "nombre": familia.nombre,
                "descripcion": familia.descripcion,
                "created_at": familia.created_at,
                "updated_at": familia.updated_at
            }
            for familia in familias
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar familias: {str(e)}"
        )

@router.get("/{familia_id}", response_model=dict)
def obtener_familia(
    familia_id: int,
    db: Session = Depends(get_db)
):
    """
    🔍 Obtener una familia específica por ID
    """
    try:
        familia_service = FamiliaService(db)
        familia = familia_service.obtener_familia(familia_id)
        if not familia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Familia no encontrada"
            )
        return {
            "id": familia.id,
            "nombre": familia.nombre,
            "descripcion": familia.descripcion,
            "created_at": familia.created_at,
            "updated_at": familia.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener familia: {str(e)}"
        )

@router.put("/{familia_id}", response_model=dict)
def actualizar_familia(
    familia_id: int,
    nombre: Optional[str] = None,
    descripcion: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    ✏️ Actualizar una familia existente
    """
    try:
        familia_service = FamiliaService(db)
        familia = familia_service.actualizar_familia(
            familia_id=familia_id,
            nombre=nombre,
            descripcion=descripcion
        )
        if not familia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Familia no encontrada"
            )
        return {
            "mensaje": "Familia actualizada exitosamente",
            "familia": {
                "id": familia.id,
                "nombre": familia.nombre,
                "descripcion": familia.descripcion
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar familia: {str(e)}"
        )

@router.delete("/{familia_id}", response_model=dict)
def eliminar_familia(
    familia_id: int,
    db: Session = Depends(get_db)
):
    """
    🗑️ Eliminar una familia (soft delete)
    """
    try:
        familia_service = FamiliaService(db)
        success = familia_service.eliminar_familia(familia_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Familia no encontrada"
            )
        return {"mensaje": "Familia eliminada exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar familia: {str(e)}"
        )

# ==========================================
# ENDPOINTS ESPECIALIZADOS
# ==========================================

@router.get("/{familia_id}/articulos", response_model=List[dict])
def obtener_articulos_familia(
    familia_id: int,
    db: Session = Depends(get_db)
):
    """
    📦 Obtener todos los artículos de una familia
    """
    try:
        familia_service = FamiliaService(db)
        articulos = familia_service.obtener_articulos_por_familia(familia_id)
        return [
            {
                "id": articulo.id,
                "nombre": articulo.nombre,
                "descripcion": articulo.descripcion,
                "sku": articulo.sku,
                "activo": articulo.activo
            }
            for articulo in articulos
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener artículos de familia: {str(e)}"
        )

@router.get("/{familia_id}/colores", response_model=List[dict])
def obtener_colores_familia(
    familia_id: int,
    db: Session = Depends(get_db)
):
    """
    🎨 Obtener todos los colores de una familia
    """
    try:
        familia_service = FamiliaService(db)
        colores = familia_service.obtener_colores_por_familia(familia_id)
        return [
            {
                "id": color.id,
                "nombre": color.nombre,
                "codigo_hex": color.codigo_hex,
                "url_imagen": color.url_imagen,
                "activo": color.activo
            }
            for color in colores
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener colores de familia: {str(e)}"
        )
