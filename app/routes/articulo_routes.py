"""
📦 Rutas para el modelo Artículo

Endpoints RESTful para gestionar los artículos.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic_core import ValidationError
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
from app.schemas.articuloDTO import ArticuloCreate, ArticuloResponse, ArticuloUpdate
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

@router.get("/", response_model=List[ArticuloResponse], responses={
    200: {'description': 'Lista de artículos obtenida exitosamente'},
    500: {'description': 'Error interno del servidor al listar artículos'}
    })
def listar_articulos(
    offset: int = 0,
    limite: int = 100,
    db: Session = Depends(get_db)
) -> List[ArticuloResponse]:
    """
    📋 Obtener lista de artículos con filtros opcionales
    """
    try:
        articulo_service = ArticuloService(db)
        articulos = articulo_service.obtener_todos(
            offset=offset,
            limite=limite
        )
        return articulos
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar artículos: {str(e)}"
        )

@router.get("/{articulo_id}", response_model=ArticuloResponse, responses={
    200: {'description': 'Artículo obtenido exitosamente'},
    404: {'description': 'Artículo no encontrado'},
    500: {'description': 'Error interno del servidor al obtener artículo'}
})
def obtener_articulo(
    articulo_id: int,
    db: Session = Depends(get_db)
) -> ArticuloResponse:
    """
    🔍 Obtener un artículo específico por ID
    """
    try:
        articulo_service = ArticuloService(db)
        articulo = articulo_service.obtener_por_id(articulo_id)
        if not articulo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artículo no encontrado"
            )
        return articulo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener artículo: {str(e)}"
        )

@router.post("/", response_model=ArticuloResponse, status_code=status.HTTP_201_CREATED, responses={
    201: {'description': 'Artículo creado exitosamente'},
    400: {'description': 'Error al crear artículo'},
    500: {'description': 'Error interno del servidor al crear artículo'}
})
def crear_articulo(
    nuevo_articulo: ArticuloCreate,
    db: Session = Depends(get_db)
) -> ArticuloResponse:
    """
    🆕 Crear un nuevo artículo
    """
    try:
        articulo_service = ArticuloService(db)
        articulo = articulo_service.crear_articulo(nuevo_articulo)
        return articulo
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Datos inválidos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear artículo: {str(e)}"
        )

@router.put("/{articulo_id}", response_model=ArticuloResponse, responses={
    200: {'description': 'Artículo actualizado exitosamente'},
    404: {'description': 'Artículo no encontrado'},
    400: {'description': 'Error al actualizar artículo'},
    500: {'description': 'Error interno del servidor al actualizar artículo'}
})
def actualizar_articulo(
    articulo_id: int,
    nuevo_articulo: ArticuloUpdate,
    db: Session = Depends(get_db)
) -> ArticuloResponse:
    """
    ✏️ Actualizar un artículo existente
    """
    try:
        articulo_service = ArticuloService(db)
        articulo = articulo_service.actualizar_articulo(articulo_id, nuevo_articulo)
        return articulo
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
) -> dict:
    """
    🗑️ Eliminar un artículo (soft delete)
    """
    try:
        articulo_service = ArticuloService(db)
        articulo_existente = articulo_service.obtener_por_id(articulo_id)
        if not articulo_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artículo no encontrado"
            )
        success = articulo_service.validar_eliminacion(articulo_id)
        if not success['puede_eliminar']:
            raise HTTPException(
                status_code=status.HTTP_400_NOT_FOUND,
                detail=f"""
                Error validando eliminación del articulo {articulo_id}:\n\t
                Razón: {success['razon']}\n\t
                Elementos relacionados: {success['elementos_relacionados']}
                """
            )
        else:
            articulo_service.eliminar_articulo(articulo_id)
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
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar artículo por SKU: {str(e)}"
        )
