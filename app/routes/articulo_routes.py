"""
📦 Rutas para el modelo Artículo

Endpoints RESTful para gestionar los artículos.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
from app.services.articulo_service import ArticuloService

router = APIRouter(prefix="/articulos", tags=["Artículos"])

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
def crear_articulo(
    nombre: str,
    id_familia: int,
    descripcion: Optional[str] = None,
    sku: Optional[str] = None,
    id_precio_venta: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    🆕 Crear un nuevo artículo
    """
    try:
        articulo_service = ArticuloService(db)
        articulo = articulo_service.crear_articulo(
            nombre=nombre,
            id_familia=id_familia,
            descripcion=descripcion,
            sku=sku,
            id_precio_venta=id_precio_venta
        )
        return {
            "mensaje": "Artículo creado exitosamente",
            "articulo": {
                "id": articulo.id,
                "nombre": articulo.nombre,
                "descripcion": articulo.descripcion,
                "sku": articulo.sku,
                "activo": articulo.activo,
                "id_familia": articulo.id_familia,
                "id_precio_venta": articulo.id_precio_venta
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear artículo: {str(e)}"
        )

@router.get("/", response_model=List[dict])
def listar_articulos(
    activo: Optional[bool] = None,
    id_familia: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    📋 Obtener lista de artículos con filtros opcionales
    """
    try:
        articulo_service = ArticuloService(db)
        articulos = articulo_service.listar_articulos(
            activo=activo,
            id_familia=id_familia,
            skip=skip,
            limit=limit
        )
        return [
            {
                "id": articulo.id,
                "nombre": articulo.nombre,
                "descripcion": articulo.descripcion,
                "sku": articulo.sku,
                "activo": articulo.activo,
                "id_familia": articulo.id_familia,
                "id_precio_venta": articulo.id_precio_venta,
                "created_at": articulo.created_at,
                "updated_at": articulo.updated_at
            }
            for articulo in articulos
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar artículos: {str(e)}"
        )

@router.get("/{articulo_id}", response_model=dict)
def obtener_articulo(
    articulo_id: int,
    db: Session = Depends(get_db)
):
    """
    🔍 Obtener un artículo específico por ID
    """
    try:
        articulo_service = ArticuloService(db)
        articulo = articulo_service.obtener_articulo(articulo_id)
        if not articulo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artículo no encontrado"
            )
        return {
            "id": articulo.id,
            "nombre": articulo.nombre,
            "descripcion": articulo.descripcion,
            "sku": articulo.sku,
            "activo": articulo.activo,
            "id_familia": articulo.id_familia,
            "id_precio_venta": articulo.id_precio_venta,
            "created_at": articulo.created_at,
            "updated_at": articulo.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener artículo: {str(e)}"
        )

@router.put("/{articulo_id}", response_model=dict)
def actualizar_articulo(
    articulo_id: int,
    nombre: Optional[str] = None,
    descripcion: Optional[str] = None,
    sku: Optional[str] = None,
    activo: Optional[bool] = None,
    id_familia: Optional[int] = None,
    id_precio_venta: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    ✏️ Actualizar un artículo existente
    """
    try:
        articulo_service = ArticuloService(db)
        articulo = articulo_service.actualizar_articulo(
            articulo_id=articulo_id,
            nombre=nombre,
            descripcion=descripcion,
            sku=sku,
            activo=activo,
            id_familia=id_familia,
            id_precio_venta=id_precio_venta
        )
        if not articulo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artículo no encontrado"
            )
        return {
            "mensaje": "Artículo actualizado exitosamente",
            "articulo": {
                "id": articulo.id,
                "nombre": articulo.nombre,
                "descripcion": articulo.descripcion,
                "sku": articulo.sku,
                "activo": articulo.activo,
                "id_familia": articulo.id_familia,
                "id_precio_venta": articulo.id_precio_venta
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar artículo: {str(e)}"
        )

@router.delete("/{articulo_id}", response_model=dict)
def eliminar_articulo(
    articulo_id: int,
    db: Session = Depends(get_db)
):
    """
    🗑️ Eliminar un artículo (soft delete)
    """
    try:
        articulo_service = ArticuloService(db)
        success = articulo_service.eliminar_articulo(articulo_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artículo no encontrado"
            )
        return {"mensaje": "Artículo eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar artículo: {str(e)}"
        )

# ==========================================
# ENDPOINTS ESPECIALIZADOS
# ==========================================

@router.get("/{articulo_id}/productos", response_model=List[dict])
def obtener_productos_articulo(
    articulo_id: int,
    db: Session = Depends(get_db)
):
    """
    🏷️ Obtener todos los productos de un artículo
    """
    try:
        articulo_service = ArticuloService(db)
        productos = articulo_service.obtener_productos_por_articulo(articulo_id)
        return [
            {
                "id": producto.id,
                "tipo_producto": producto.tipo_producto,
                "id_articulo": producto.id_articulo,
                "created_at": producto.created_at,
                "updated_at": producto.updated_at
            }
            for producto in productos
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos del artículo: {str(e)}"
        )

@router.get("/{articulo_id}/packs", response_model=List[dict])
def obtener_packs_articulo(
    articulo_id: int,
    db: Session = Depends(get_db)
):
    """
    📦 Obtener todos los packs de un artículo
    """
    try:
        articulo_service = ArticuloService(db)
        packs = articulo_service.obtener_packs_por_articulo(articulo_id)
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener packs del artículo: {str(e)}"
        )

@router.get("/buscar/sku/{sku}", response_model=dict)
def buscar_articulo_por_sku(
    sku: str,
    db: Session = Depends(get_db)
):
    """
    🔍 Buscar un artículo por su SKU
    """
    try:
        articulo_service = ArticuloService(db)
        articulo = articulo_service.buscar_por_sku(sku)
        if not articulo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artículo con SKU no encontrado"
            )
        return {
            "id": articulo.id,
            "nombre": articulo.nombre,
            "descripcion": articulo.descripcion,
            "sku": articulo.sku,
            "activo": articulo.activo,
            "id_familia": articulo.id_familia,
            "id_precio_venta": articulo.id_precio_venta
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar artículo por SKU: {str(e)}"
        )
