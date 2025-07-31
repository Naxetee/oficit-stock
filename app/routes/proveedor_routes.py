"""
🏢 Rutas para el modelo Proveedor

Endpoints RESTful para gestionar los proveedores.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
from app.schemas.proveedorDTO import ProveedorCreate, ProveedorResponse, ProveedorUpdate
from app.services.proveedor_service import ProveedorService

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# ENDPOINTS CRUD BÁSICOS
# ==========================================

@router.post("/", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED, responses={
    201: {"description": "Proveedor creado exitosamente"},
    400: {"description": "Error al crear proveedor"},
    500: {"description": "Error interno del servidor"}
    })
def crear_proveedor(
    nuevo_proveedor: ProveedorCreate,
    db: Session = Depends(get_db)
):
    """
    🆕 Crear un nuevo proveedor
    """
    try:
        proveedor_service = ProveedorService(db)
        return proveedor_service.crear_proveedor(nuevo_proveedor)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear proveedor: {str(e)}"
        )

@router.get("/", response_model=List[ProveedorResponse], status_code=status.HTTP_200_OK, responses={
    200: {"description": "Lista de proveedores obtenida exitosamente"},
    500: {"description": "Error interno del servidor"}
    })
def listar_proveedores(
    offset: int = 0,
    limite: int = 100,
    db: Session = Depends(get_db)
):
    """
    📋 Obtener lista de proveedores con filtros opcionales
    """
    try:
        proveedor_service = ProveedorService(db)
        proveedores = proveedor_service.obtener_todos(
            offset=offset,
            limite=limite
        )
        return proveedores
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar proveedores: {str(e)}"
        )

@router.get("/{proveedor_id}", response_model=ProveedorResponse, status_code=status.HTTP_200_OK, responses={
    200: {"description": "Proveedor encontrado exitosamente"},
    404: {"description": "Proveedor no encontrado"},
    500: {"description": "Error interno del servidor"}
    })
def obtener_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):
    """
    🔍 Obtener un proveedor específico por ID
    """
    try:
        proveedor_service = ProveedorService(db)
        proveedor = proveedor_service.obtener_por_id(proveedor_id)
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor no encontrado"
            )
        return proveedor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener proveedor: {str(e)}"
        )

@router.put("/{proveedor_id}", response_model=ProveedorResponse, status_code=status.HTTP_200_OK, responses={
    200: {"description": "Proveedor actualizado exitosamente"},
    404: {"description": "Proveedor no encontrado"},
    400: {"description": "Error al actualizar proveedor"},
    500: {"description": "Error interno del servidor"}
    })
def actualizar_proveedor(
    proveedor_id: int,
    nuevo_proveedor: ProveedorUpdate,
    db: Session = Depends(get_db)
):
    """
    ✏️ Actualizar un proveedor existente
    """
    try:
        proveedor_service = ProveedorService(db)
        proveedor = proveedor_service.actualizar_proveedor(proveedor_id, nuevo_proveedor)
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor no encontrado"
            )
        return proveedor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar proveedor: {str(e)}"
        )

@router.delete("/{proveedor_id}", response_model=dict, status_code=status.HTTP_200_OK, responses={
    200: {"description": "Proveedor eliminado exitosamente"},
    404: {"description": "Proveedor no encontrado"},
    400: {"description": "Error al eliminar proveedor"},
    500: {"description": "Error interno del servidor"}
    })
def eliminar_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):
    """
    🗑️ Eliminar un proveedor (soft delete)
    """
    try:
        proveedor_service = ProveedorService(db)
        success = proveedor_service.eliminar(proveedor_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor no encontrado"
            )
        return {"detail": "Proveedor eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar proveedor: {str(e)}"
        )

# ==========================================
# ENDPOINTS ESPECIALIZADOS
# ==========================================

@router.get("/{proveedor_id}/componentes", response_model=List[dict])
def obtener_componentes_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):
    """
    🔧 Obtener todos los componentes de un proveedor
    """
    try:
        proveedor_service = ProveedorService(db)
        componentes = proveedor_service.obtener_componentes_por_proveedor(proveedor_id)
        return [
            {
                "id": componente.id,
                "nombre": componente.nombre,
                "descripcion": componente.descripcion,
                "codigo": componente.codigo,
                "especificaciones": componente.especificaciones
            }
            for componente in componentes
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener componentes del proveedor: {str(e)}"
        )
