"""
🏢 Rutas para el modelo Proveedor

Endpoints RESTful para gestionar los proveedores.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
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

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_proveedor(
    nombre: str,
    nif: Optional[str] = None,
    direccion: Optional[str] = None,
    telefono: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    🆕 Crear un nuevo proveedor
    """
    try:
        proveedor_service = ProveedorService(db)
        proveedor = proveedor_service.crear_proveedor(
            nombre=nombre,
            nif=nif,
            direccion=direccion,
            telefono=telefono,
            email=email
        )
        return {
            "mensaje": "Proveedor creado exitosamente",
            "proveedor": {
                "id": proveedor.id,
                "nombre": proveedor.nombre,
                "nif_cif": proveedor.nif_cif,
                "direccion": proveedor.direccion,
                "telefono": proveedor.telefono,
                "email": proveedor.email,
                "activo": proveedor.activo
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear proveedor: {str(e)}"
        )

@router.get("/", response_model=List[dict])
def listar_proveedores(
    activo: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    📋 Obtener lista de proveedores con filtros opcionales
    """
    try:
        proveedor_service = ProveedorService(db)
        proveedores = proveedor_service.listar_proveedores(
            activo=activo,
            skip=skip,
            limit=limit
        )
        return [
            {
                "id": proveedor.id,
                "nombre": proveedor.nombre,
                "nif_cif": proveedor.nif_cif,
                "direccion": proveedor.direccion,
                "telefono": proveedor.telefono,
                "email": proveedor.email,
                "activo": proveedor.activo,
                "created_at": proveedor.created_at,
                "updated_at": proveedor.updated_at
            }
            for proveedor in proveedores
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar proveedores: {str(e)}"
        )

@router.get("/{proveedor_id}", response_model=dict)
def obtener_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):
    """
    🔍 Obtener un proveedor específico por ID
    """
    try:
        proveedor_service = ProveedorService(db)
        proveedor = proveedor_service.obtener_proveedor(proveedor_id)
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor no encontrado"
            )
        return {
            "id": proveedor.id,
            "nombre": proveedor.nombre,
            "nif_cif": proveedor.nif_cif,
            "direccion": proveedor.direccion,
            "telefono": proveedor.telefono,
            "email": proveedor.email,
            "activo": proveedor.activo,
            "created_at": proveedor.created_at,
            "updated_at": proveedor.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener proveedor: {str(e)}"
        )

@router.put("/{proveedor_id}", response_model=dict)
def actualizar_proveedor(
    proveedor_id: int,
    nombre: Optional[str] = None,
    nif: Optional[str] = None,
    direccion: Optional[str] = None,
    telefono: Optional[str] = None,
    email: Optional[str] = None,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    ✏️ Actualizar un proveedor existente
    """
    try:
        proveedor_service = ProveedorService(db)
        proveedor = proveedor_service.actualizar_proveedor(
            proveedor_id=proveedor_id,
            nombre=nombre,
            nif=nif,
            direccion=direccion,
            telefono=telefono,
            email=email,
            activo=activo
        )
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor no encontrado"
            )
        return {
            "mensaje": "Proveedor actualizado exitosamente",
            "proveedor": {
                "id": proveedor.id,
                "nombre": proveedor.nombre,
                "nif_cif": proveedor.nif_cif,
                "direccion": proveedor.direccion,
                "telefono": proveedor.telefono,
                "email": proveedor.email,
                "activo": proveedor.activo
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar proveedor: {str(e)}"
        )

@router.delete("/{proveedor_id}", response_model=dict)
def eliminar_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):
    """
    🗑️ Eliminar un proveedor (soft delete)
    """
    try:
        proveedor_service = ProveedorService(db)
        success = proveedor_service.eliminar_proveedor(proveedor_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proveedor no encontrado"
            )
        return {"mensaje": "Proveedor eliminado exitosamente"}
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
