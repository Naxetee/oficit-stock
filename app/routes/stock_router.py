from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.movimiento_schema import MovimientoCreate, MovimientoResponse
from app.schemas.stock_schema import StockResponse
from ..services import get_MovimientoService, get_StockService
from ..db import get_db

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.get("/", response_model=List[StockResponse], responses={
    200: {"description": "Lista de stocks"},
    422: {"description": "Error de validación"}
})
def listar_stock(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de artículo"),
    ubicacion: Optional[str] = Query(None, description="Filtrar por ubicación"),
    bajo_stock: Optional[bool] = Query(None, description="Filtrar por bajo stock"),
):
    service = get_StockService()(db)
    if bajo_stock:
        return service.obtener_alertas(tipo=tipo, ubicacion=ubicacion)
    return service.obtener_todos(
        skip=skip,
        limit=limit,
        filtros={
            "tipo": tipo,
            "ubicacion": ubicacion,
        }
    )

@router.get("/componente/{id}", response_model=StockResponse, responses={
    200: {"description": "Stock encontrado"},
    404: {"description": "Stock no encontrado"},
    422: {"description": "Error de validación"}
})
def obtener_stock_por_componente(id: int, db: Session = Depends(get_db)):
    service = get_StockService()(db)
    result = service.obtener_por_id_componente(id)
    return result

@router.get("/producto_simple/{id}", response_model=StockResponse, responses={
    200: {"description": "Stock encontrado"},
    404: {"description": "Stock no encontrado"},
    422: {"description": "Error de validación"}
})
def obtener_stock_por_producto_simple(id: int, db: Session = Depends(get_db)):
    service = get_StockService()(db)
    result = service.obtener_por_id_producto_simple(id)
    return result

@router.get("/movimiento", response_model=List[MovimientoResponse], responses={
    200: {"description": "Lista de movimientos"},
    422: {"description": "Error de validación"}
})
def listar_movimientos(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0, description="Número de registros a saltar"),
        limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
        tipo: Optional[str] = Query(None, description="Filtrar por tipo de movimiento (entrada/salida)"),
        componente_id: Optional[int] = Query(None, description="Filtrar por ID de componente"),
        producto_simple_id: Optional[int] = Query(None, description="Filtrar por ID de producto simple")
    ):
    movimiento_service = get_MovimientoService()(db)
    return movimiento_service.obtener_todos(
        skip=skip,
        limit=limit,
        filtros={
            "tipo": tipo,
            "id_componente": componente_id,
            "id_producto_simple": producto_simple_id
        }
    )

@router.post("/movimiento", response_model=StockResponse, status_code=201, responses={
    201: {"description": "Stock creado"},
    422: {"description": "Error de validación"}
})
def crear_movimiento(data: MovimientoCreate, db: Session = Depends(get_db)):
    movimiento_service = get_MovimientoService()(db)
    return movimiento_service.crear_movimiento(data)

@router.delete("/movimiento/{id}", responses={
    200: {"description": "Movimiento eliminado"},
    404: {"description": "Movimiento no encontrado"},
    422: {"description": "Error de validación"}
})
def eliminar_movimiento(id: int, db: Session = Depends(get_db)):
    movimiento_service = get_MovimientoService()(db)
    result = movimiento_service.eliminar(id)
    return {"detail": "Movimiento eliminado exitosamente"}