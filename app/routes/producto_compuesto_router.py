from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.producto_compuesto_schema import ProductoCompuestoResponse, ProductoCompuestoCreate, ProductoCompuestoUpdate
from ..services import get_ProductoCompuestoService
from ..db import get_db

router = APIRouter(prefix="/producto-compuesto", tags=["ProductoCompuesto"])

@router.get("/", response_model=list[ProductoCompuestoResponse], responses={
    200: {"description": "Lista de productos compuestos"},
    422: {"description": "Error de validación"}
})
def get_all(db: Session = Depends(get_db)):
    service = get_ProductoCompuestoService()(db)
    return service.obtener_todos()

@router.get("/{id}", response_model=ProductoCompuestoResponse, responses={
    200: {"description": "Producto compuesto encontrado"},
    404: {"description": "Producto compuesto no encontrado"},
    422: {"description": "Error de validación"}
})
def get_by_id(id: int, db: Session = Depends(get_db)):
    service = get_ProductoCompuestoService()(db)
    result = service.obtener_por_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Producto compuesto no encontrado")
    return result

@router.post("/", response_model=ProductoCompuestoResponse, responses={
    201: {"description": "Producto compuesto creado"},
    422: {"description": "Error de validación"}
})
def create(data: ProductoCompuestoCreate, db: Session = Depends(get_db)):
    service = get_ProductoCompuestoService()(db)
    return service.crear(data)

@router.put("/{id}", response_model=ProductoCompuestoResponse, responses={
    200: {"description": "Producto compuesto actualizado"},
    404: {"description": "Producto compuesto no encontrado"},
    422: {"description": "Error de validación"}
})
def update(id: int, data: ProductoCompuestoUpdate, db: Session = Depends(get_db)):
    service = get_ProductoCompuestoService()(db)
    result = service.actualizar(id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Producto compuesto no encontrado")
    return result

@router.delete("/{id}", responses={
    200: {"description": "Producto compuesto eliminado"},
    404: {"description": "Producto compuesto no encontrado"},
    422: {"description": "Error de validación"}
})
def delete(id: int, db: Session = Depends(get_db)):
    service = get_ProductoCompuestoService()(db)
    return service.eliminar(id)
