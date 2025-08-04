from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.producto_simple_schema import ProductoSimpleResponse, ProductoSimpleCreate, ProductoSimpleUpdate
from ..services import get_ProductoSimpleService
from ..db import get_db

router = APIRouter(prefix="/producto-simple", tags=["ProductoSimple"])

@router.get("/", response_model=list[ProductoSimpleResponse], responses={
    200: {"description": "Lista de productos simples"},
    422: {"description": "Error de validación"}
})
def get_all(db: Session = Depends(get_db)):
    service = get_ProductoSimpleService()(db)
    return service.obtener_todos()

@router.get("/{id}", response_model=ProductoSimpleResponse, responses={
    200: {"description": "Producto simple encontrado"},
    404: {"description": "Producto simple no encontrado"},
    422: {"description": "Error de validación"}
})
def get_by_id(id: int, db: Session = Depends(get_db)):
    service = get_ProductoSimpleService()(db)
    result = service.obtener_por_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Producto simple no encontrado")
    return result

@router.post("/", response_model=ProductoSimpleResponse, responses={
    201: {"description": "Producto simple creado"},
    422: {"description": "Error de validación"}
})
def create(data: ProductoSimpleCreate, db: Session = Depends(get_db)):
    service = get_ProductoSimpleService()(db)
    return service.crear(data)

@router.put("/{id}", response_model=ProductoSimpleResponse, responses={
    200: {"description": "Producto simple actualizado"},
    404: {"description": "Producto simple no encontrado"},
    422: {"description": "Error de validación"}
})
def update(id: int, data: ProductoSimpleUpdate, db: Session = Depends(get_db)):
    service = get_ProductoSimpleService()(db)
    result = service.actualizar(id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Producto simple no encontrado")
    return result

@router.delete("/{id}", responses={
    200: {"description": "Producto simple eliminado"},
    404: {"description": "Producto simple no encontrado"},
    422: {"description": "Error de validación"}
})
def delete(id: int, db: Session = Depends(get_db)):
    service = get_ProductoSimpleService()(db)
    return service.eliminar(id)
