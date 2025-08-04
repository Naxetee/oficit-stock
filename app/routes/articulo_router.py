from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.articulo_schema import ArticuloResponse
from ..services import get_ProductoCompuestoService, get_ProductoSimpleService, get_PackService
from ..db import get_db

router = APIRouter(prefix="/articulos", tags=["Articulos"])

@router.get("/", response_model=Dict[str, List[ArticuloResponse]], responses={
    200: {"description": "Lista de artículos"},
    422: {"description": "Error de validación"}
})
def listar_articulos(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    familia_id: Optional[int] = Query(None, description="Filtrar por familia"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo (simple, compuesto, pack)"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    codigo_tienda: Optional[str] = Query(None, description="Buscar por código de tienda"),
    nombre: Optional[str] = Query(None, description="Buscar por nombre (búsqueda parcial)")
):
    services = {
        "producto_compuesto": get_ProductoCompuestoService()(db),
        "producto_simple": get_ProductoSimpleService()(db),
        "pack": get_PackService()(db)
    }

    result = {}
    for key, service in services.items():
        result[key] = service.obtener_todos(
            skip=skip,
            limit=limit,
            filtros={
                "id_familia": familia_id,
                "tipo": tipo,
                "activo": activo,
                "codigo_tienda": codigo_tienda,
                "nombre": nombre
            }
        )

    return result

@router.get("/{id}", response_model=ArticuloResponse, responses={
    200: {"description": "Artículo encontrado"},
    404: {"description": "Artículo no encontrado"}
})
def obtener_articulo_por_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un artículo por su ID.
    """
    services = {
        "producto_compuesto": get_ProductoCompuestoService()(db),
        "producto_simple": get_ProductoSimpleService()(db),
        "pack": get_PackService()(db)
    }

    for service in services.values():
        articulo = service.obtener_por_id(id)
        if articulo:
            return articulo

    raise HTTPException(status_code=404, detail="Artículo no encontrado")