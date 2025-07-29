"""
📦 Rutas para el modelo Pack

Endpoints RESTful para gestionar packs de productos.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
from app.services.pack_service import PackService

router = APIRouter(prefix="/packs", tags=["Packs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_pack(
    nombre: str,
    id_articulo: int,
    descripcion: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """🆕 Crear un nuevo pack"""
    try:
        pack_service = PackService(db)
        pack = pack_service.crear_pack(
            nombre=nombre,
            id_articulo=id_articulo,
            descripcion=descripcion
        )
        return {
            "mensaje": "Pack creado exitosamente",
            "pack": {
                "id": pack.id,
                "nombre": pack.nombre,
                "descripcion": pack.descripcion,
                "id_articulo": pack.id_articulo
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear pack: {str(e)}")

@router.get("/", response_model=List[dict])
def listar_packs(
    id_articulo: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """📋 Obtener lista de packs con filtros opcionales"""
    try:
        pack_service = PackService(db)
        packs = pack_service.listar_packs(
            id_articulo=id_articulo,
            skip=skip,
            limit=limit
        )
        return [
            {
                "id": pack.id,
                "nombre": pack.nombre,
                "descripcion": pack.descripcion,
                "id_articulo": pack.id_articulo,
                "created_at": pack.created_at,
                "updated_at": pack.updated_at
            }
            for pack in packs
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al listar packs: {str(e)}")

@router.get("/{pack_id}", response_model=dict)
def obtener_pack(pack_id: int, db: Session = Depends(get_db)):
    """🔍 Obtener un pack específico por ID"""
    try:
        pack_service = PackService(db)
        pack = pack_service.obtener_pack(pack_id)
        if not pack:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pack no encontrado")
        return {
            "id": pack.id,
            "nombre": pack.nombre,
            "descripcion": pack.descripcion,
            "id_articulo": pack.id_articulo,
            "created_at": pack.created_at,
            "updated_at": pack.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener pack: {str(e)}")

@router.put("/{pack_id}", response_model=dict)
def actualizar_pack(
    pack_id: int,
    nombre: Optional[str] = None,
    descripcion: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """✏️ Actualizar un pack existente"""
    try:
        pack_service = PackService(db)
        pack = pack_service.actualizar_pack(
            pack_id=pack_id,
            nombre=nombre,
            descripcion=descripcion
        )
        if not pack:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pack no encontrado")
        return {
            "mensaje": "Pack actualizado exitosamente",
            "pack": {
                "id": pack.id,
                "nombre": pack.nombre,
                "descripcion": pack.descripcion
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al actualizar pack: {str(e)}")

@router.delete("/{pack_id}", response_model=dict)
def eliminar_pack(pack_id: int, db: Session = Depends(get_db)):
    """🗑️ Eliminar un pack"""
    try:
        pack_service = PackService(db)
        success = pack_service.eliminar_pack(pack_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pack no encontrado")
        return {"mensaje": "Pack eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al eliminar pack: {str(e)}")

@router.get("/{pack_id}/productos", response_model=List[dict])
def obtener_productos_pack(pack_id: int, db: Session = Depends(get_db)):
    """🏷️ Obtener productos incluidos en un pack"""
    try:
        pack_service = PackService(db)
        productos = pack_service.obtener_productos_pack(pack_id)
        return [
            {
                "id": rel.id,
                "cantidad_incluida": float(rel.cantidad_incluida),
                "producto": {
                    "id": rel.producto.id,
                    "tipo_producto": rel.producto.tipo_producto,
                    "id_articulo": rel.producto.id_articulo
                }
            }
            for rel in productos
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener productos del pack: {str(e)}")

@router.post("/{pack_id}/productos/{producto_id}", response_model=dict)
def agregar_producto_a_pack(
    pack_id: int,
    producto_id: int,
    cantidad_incluida: float,
    db: Session = Depends(get_db)
):
    """➕ Agregar producto a pack"""
    try:
        pack_service = PackService(db)
        relacion = pack_service.agregar_producto_a_pack(pack_id, producto_id, cantidad_incluida)
        return {
            "mensaje": "Producto agregado al pack exitosamente",
            "relacion": {
                "id": relacion.id,
                "cantidad_incluida": float(relacion.cantidad_incluida)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al agregar producto al pack: {str(e)}")
