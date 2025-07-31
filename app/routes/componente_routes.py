"""
🔧 Rutas para el modelo Componente

Endpoints RESTful para gestionar los componentes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
from app.services.componente_service import ComponenteService

router = APIRouter(prefix="/componentes", tags=["Componentes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_componente(
    nombre: str,
    descripcion: Optional[str] = None,
    codigo: Optional[str] = None,
    especificaciones: Optional[str] = None,
    id_proveedor: Optional[int] = None,
    id_color: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """🆕 Crear un nuevo componente"""
    try:
        componente_service = ComponenteService(db)
        componente = componente_service.crear_componente(
            nombre=nombre,
            descripcion=descripcion,
            codigo=codigo,
            especificaciones=especificaciones,
            id_proveedor=id_proveedor,
            id_color=id_color
        )
        return {
            "mensaje": "Componente creado exitosamente",
            "componente": {
                "id": componente.id,
                "nombre": componente.nombre,
                "descripcion": componente.descripcion,
                "codigo": componente.codigo,
                "especificaciones": componente.especificaciones,
                "id_proveedor": componente.id_proveedor,
                "id_color": componente.id_color
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear componente: {str(e)}")

@router.get("/", response_model=List[dict])
def listar_componentes(
    id_proveedor: Optional[int] = None,
    id_color: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """📋 Obtener lista de componentes con filtros opcionales"""
    try:
        componente_service = ComponenteService(db)
        componentes = componente_service.listar_componentes(
            id_proveedor=id_proveedor,
            id_color=id_color,
            skip=skip,
            limit=limit
        )
        return [
            {
                "id": componente.id,
                "nombre": componente.nombre,
                "descripcion": componente.descripcion,
                "codigo": componente.codigo,
                "especificaciones": componente.especificaciones,
                "id_proveedor": componente.id_proveedor,
                "id_color": componente.id_color,
                "created_at": componente.created_at,
                "updated_at": componente.updated_at
            }
            for componente in componentes
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al listar componentes: {str(e)}")

@router.get("/{componente_id}", response_model=dict)
def obtener_componente(componente_id: int, db: Session = Depends(get_db)):
    """🔍 Obtener un componente específico por ID"""
    try:
        componente_service = ComponenteService(db)
        componente = componente_service.obtener_componente(componente_id)
        if not componente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Componente no encontrado")
        return {
            "id": componente.id,
            "nombre": componente.nombre,
            "descripcion": componente.descripcion,
            "codigo": componente.codigo,
            "especificaciones": componente.especificaciones,
            "id_proveedor": componente.id_proveedor,
            "id_color": componente.id_color,
            "created_at": componente.created_at,
            "updated_at": componente.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener componente: {str(e)}")

@router.put("/{componente_id}", response_model=dict)
def actualizar_componente(
    componente_id: int,
    nombre: Optional[str] = None,
    descripcion: Optional[str] = None,
    codigo: Optional[str] = None,
    especificaciones: Optional[str] = None,
    id_proveedor: Optional[int] = None,
    id_color: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """✏️ Actualizar un componente existente"""
    try:
        componente_service = ComponenteService(db)
        componente = componente_service.actualizar_componente(
            componente_id=componente_id,
            nombre=nombre,
            descripcion=descripcion,
            codigo=codigo,
            especificaciones=especificaciones,
            id_proveedor=id_proveedor,
            id_color=id_color
        )
        if not componente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Componente no encontrado")
        return {"mensaje": "Componente actualizado exitosamente", "componente": {"id": componente.id, "nombre": componente.nombre}}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al actualizar componente: {str(e)}")

@router.delete("/{componente_id}", response_model=dict)
def eliminar_componente(componente_id: int, db: Session = Depends(get_db)):
    """🗑️ Eliminar un componente"""
    try:
        componente_service = ComponenteService(db)
        success = componente_service.eliminar_componente(componente_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Componente no encontrado")
        return {"mensaje": "Componente eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al eliminar componente: {str(e)}")
