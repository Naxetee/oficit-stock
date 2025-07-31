"""
📦 Rutas para el modelo Articulo

Endpoints RESTful para gestionar los Articulos.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic_core import ValidationError
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
from app.schemas.articuloDTO import ArticuloCreate, ArticuloResponse, ArticuloUpdate
from app.services.articulo_service import ArticuloService

router = APIRouter(prefix="/articulos", tags=["Articulos"])

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
    200: {'description': 'Lista de Articulos obtenida exitosamente'},
    500: {'description': 'Error interno del servidor al listar Articulos'}
    })
def listar_articulos(
    offset: int = 0,
    limite: int = 100,
    db: Session = Depends(get_db)
) -> List[ArticuloResponse]:
    """
    📋 Obtener lista de Articulos con filtros opcionales
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
            detail=f"Error al listar Articulos: {str(e)}"
        )

@router.get("/{articulo_id}", response_model=ArticuloResponse, responses={
    200: {'description': 'Articulo obtenido exitosamente'},
    404: {'description': 'Articulo no encontrado'},
    500: {'description': 'Error interno del servidor al obtener Articulo'}
})
def obtener_articulo(
    articulo_id: int,
    db: Session = Depends(get_db)
) -> ArticuloResponse:
    """
    🔍 Obtener un Articulo específico por ID
    """
    try:
        articulo_service = ArticuloService(db)
        articulo = articulo_service.obtener_por_id(articulo_id)
        if not articulo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Articulo no encontrado"
            )
        return articulo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener Articulo: {str(e)}"
        )

@router.post("/", response_model=ArticuloResponse, status_code=status.HTTP_201_CREATED, responses={
    201: {'description': 'Articulo creado exitosamente'},
    400: {'description': 'Error al crear Articulo'},
    500: {'description': 'Error interno del servidor al crear Articulo'}
})
def crear_articulo(
    nuevo_articulo: ArticuloCreate,
    db: Session = Depends(get_db)
) -> ArticuloResponse:
    """
    🆕 Crear un nuevo Articulo
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
            detail=f"Error al crear Articulo: {str(e)}"
        )

@router.put("/{articulo_id}", response_model=ArticuloResponse, responses={
    200: {'description': 'Articulo actualizado exitosamente'},
    404: {'description': 'Articulo no encontrado'},
    400: {'description': 'Error al actualizar Articulo'},
    500: {'description': 'Error interno del servidor al actualizar Articulo'}
})
def actualizar_articulo(
    articulo_id: int,
    nuevo_articulo: ArticuloUpdate,
    db: Session = Depends(get_db)
) -> ArticuloResponse:
    """
    ✏️ Actualizar un Articulo existente
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
            detail=f"Error al actualizar Articulo: {str(e)}"
        )

@router.delete("/{articulo_id}", response_model=dict)
def eliminar_articulo(
    articulo_id: int,
    db: Session = Depends(get_db)
) -> dict:
    """
    🗑️ Eliminar un Articulo (soft delete)
    """
    try:
        articulo_service = ArticuloService(db)
        articulo_existente = articulo_service.obtener_por_id(articulo_id)
        if not articulo_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Articulo no encontrado"
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
            articulo_service.eliminar(articulo_id)
        return {"detail": "Articulo eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar Articulo: {str(e)}"
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
    🏷️ Obtener todos los productos de un Articulo
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
            detail=f"Error al obtener productos del Articulo: {str(e)}"
        )

@router.get("/{articulo_id}/packs", response_model=List[dict])
def obtener_packs_articulo(
    articulo_id: int,
    db: Session = Depends(get_db)
):
    """
    📦 Obtener todos los packs de un Articulo
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
            detail=f"Error al obtener packs del Articulo: {str(e)}"
        )

@router.get("/buscar/sku/{sku}", response_model=dict)
def buscar_articulo_por_sku(
    sku: str,
    db: Session = Depends(get_db)
):
    """
    🔍 Buscar un Articulo por su SKU
    """
    try:
        articulo_service = ArticuloService(db)
        articulo = articulo_service.buscar_por_sku(sku)
        if not articulo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Articulo con SKU no encontrado"
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
            detail=f"Error al buscar Articulo por SKU: {str(e)}"
        )
