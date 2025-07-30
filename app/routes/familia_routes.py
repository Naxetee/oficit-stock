"""
🏷️ Rutas para el modelo Familia

Endpoints RESTful para gestionar las familias de productos.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing import List
from app.db import SessionLocal
from app.schemas.articuloDTO import ArticuloInDB
from app.schemas.colorDTO import ColorInDB
from app.schemas.familiaDTO import FamiliaInDB, FamiliaCreate, FamiliaUpdate
from app.services.familia_service import FamiliaService

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

@router.get("/", response_model=List[FamiliaInDB], responses={
    200: {"description": "Lista de familias obtenida exitosamente"},
    500: {"description": "Error interno del servidor"}
})
def listar_familias(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    📋 Obtener lista de familias con filtros opcionales

    - **offset**: Número de registros a omitir (paginación).
    - **limit**: Número máximo de registros a retornar (paginación).
    """
    try:
        familia_service = FamiliaService(db)
        familias = familia_service.obtener_todos(
            offset=offset,
            limite=limit
        )
        return familias
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar familias: {str(e)}"
        )
    

@router.get("/{familia_id}", response_model=FamiliaInDB, responses={
    200: {"description": "Familia encontrada"},
    404: {"description": "Familia no encontrada"},
    500: {"description": "Error interno del servidor"}
})
def obtener_familia(
    familia_id: int,
    db: Session = Depends(get_db)
):
    """
    🔍 Obtener una familia específica por ID

    - **familia_id**: ID de la familia a obtener
    """
    try:
        familia_service = FamiliaService(db)
        familia = familia_service.obtener_por_id(familia_id)
        if not familia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Familia no encontrada"
            )
        return familia
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener familia: {str(e)}"
        )

        
@router.post("/", response_model=FamiliaInDB, status_code=status.HTTP_201_CREATED, responses={
    201: {"description": "Familia creada exitosamente"},
    400: {"description": "Error en los datos enviados o familia duplicada"}
})
def crear_familia(
    nueva_familia: FamiliaCreate,
    db: Session = Depends(get_db)
):
    """
    🆕 Crear una nueva familia de productos

    - **nueva_familia**: Datos de la familia a crear.
    """
    try:
        familia_service = FamiliaService(db)
        familia = familia_service.crear_familia(nueva_familia)
        return familia
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Datos inválidos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear familia: {str(e)}"
        )


@router.put("/{familia_id}", response_model=FamiliaInDB, responses={
    200: {"description": "Familia actualizada exitosamente"},
    400: {"description": "Error en los datos enviados"},
    404: {"description": "Familia no encontrada"}
})
def actualizar_familia(
    familia_id: int,
    nueva_familia: FamiliaUpdate,
    db: Session = Depends(get_db)
):
    """
    ✏️ Actualizar una familia existente

    - **familia_id**: ID de la familia a actualizar.
    - **nueva_familia**: Datos actualizados de la familia.
    """
    try:
        familia_service = FamiliaService(db)
        
        # Usar el método específico de actualización
        familia_actualizada = familia_service.actualizar_familia(familia_id, nueva_familia)
        
        return familia_actualizada
        
    except ValueError as e:
        # Error de validación de negocio (familia no existe, nombre duplicado, etc.)
        if "No se encontró" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar familia: {str(e)}"
        )

@router.delete("/{familia_id}", response_model=dict, responses={
    200: {"description": "Familia eliminada exitosamente"},
    400: {"description": "Error al eliminar - familia tiene dependencias"},
    404: {"description": "Familia no encontrada"},
    409: {"description": "Conflicto - familia tiene elementos relacionados"}
})
def eliminar_familia(
    familia_id: int,
    db: Session = Depends(get_db)
):
    """
    🗑️ Eliminar una familia (soft delete)

    - **familia_id**: ID de la familia a eliminar.
    """
    try:
        familia_service = FamiliaService(db)
        familia = familia_service.obtener_por_id(familia_id)
        if not familia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Familia no encontrada"
            )
        success = familia_service.validar_eliminacion(familia_id)
        if not success['puede_eliminar']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error validando eliminación de la familia {familia_id}:\n\tRazón: {success['razon']}\n\tElementos relacionados: {success['elementos_relacionados']}"
            )
        else:        
            success = familia_service.eliminar(id=familia_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Familia no encontrada"
            )
        return {"detail": "Familia eliminada exitosamente"}
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

@router.get("/{familia_id}/articulos", response_model=List[ArticuloInDB], responses={
    200: {"description": "Lista de artículos de la familia"},
    404: {"description": "Familia no encontrada"},
    500: {"description": "Error interno del servidor"}
})
def obtener_articulos_familia(
    familia_id: int,
    db: Session = Depends(get_db)
):
    """
    📦 Obtener todos los artículos de una familia

    - **familia_id**: ID de la familia a obtener los artículos.
    """
    try:
        familia_service = FamiliaService(db)
        return familia_service.obtener_articulos_por_familia(familia_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener artículos de familia: {str(e)}"
        )


@router.get("/{familia_id}/colores", response_model=List[ColorInDB], responses={
    200: {"description": "Lista de colores de la familia"},
    404: {"description": "Familia no encontrada"},
    500: {"description": "Error interno del servidor"}
})
def obtener_colores_familia(
    familia_id: int,
    db: Session = Depends(get_db)
):
    """
    🎨 Obtener todos los colores de una familia

    - **familia_id**: ID de la familia a obtener los colores.
    """
    try:
        familia_service = FamiliaService(db)
        colores = familia_service.obtener_colores_por_familia(familia_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener colores de familia: {str(e)}"
        )
    if not colores:
        return []
    return colores

@router.get("/{familia_id}/estadisticas", response_model=dict, responses={
    200: {"description": "Estadísticas de la familia"},
    404: {"description": "Familia no encontrada"},
    500: {"description": "Error interno del servidor"}
})
def obtener_estadisticas_familia(
    familia_id: int,
    db: Session = Depends(get_db)
):
    """
    📊 Obtener estadísticas de una familia

    - **familia_id**: ID de la familia a obtener las estadísticas.
    """
    try:
        familia_service = FamiliaService(db)
        estadisticas = familia_service.obtener_estadisticas_familia(familia_id)
        if not estadisticas:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Familia no encontrada"
            )
        return estadisticas
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas de familia: {str(e)}"
        )

@router.get("/buscar", response_model=List[FamiliaInDB], responses={
    200: {"description": "Resultados de búsqueda"},
    400: {"description": "Parámetros de búsqueda inválidos"},
    500: {"description": "Error interno del servidor"}
})
def buscar_familias_por_texto(
    texto: str,
    db: Session = Depends(get_db)
):
    """
    🔎 Buscar familias por texto

    - **texto**: Texto para buscar coincidencias en familias.
    """
    try:
        familia_service = FamiliaService(db)
        familias = familia_service.buscar_familias_por_texto(texto)
        return [FamiliaInDB.model_validate(familia).model_dump() for familia in familias]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar familias: {str(e)}"
        )