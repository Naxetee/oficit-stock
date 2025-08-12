from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.proveedor_schema import ProveedorResponse, ProveedorCreate, ProveedorUpdate
from ..services import get_ProveedorService
from ..db import get_db

router = APIRouter(prefix="/proveedor", tags=["Proveedor"])

@router.get("/", response_model=list[ProveedorResponse], responses={
    200: {"description": "Lista de proveedores"},
    400: {"description": "Error de petición"},
    422: {"description": "Error de validación"}
})
def get_all(db: Session = Depends(get_db)):
    service = get_ProveedorService()(db)
    return service.obtener_todos()

@router.get("/{id}", response_model=ProveedorResponse, responses={
    200: {"description": "Proveedor encontrado"},
    400: {"description": "Error de petición"},
    404: {"description": "Proveedor no encontrado"},
    422: {"description": "Error de validación"}
})
def get_by_id(id: int, db: Session = Depends(get_db)):
    service = get_ProveedorService()(db)
    result = service.obtener_por_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return result

@router.post("/", response_model=ProveedorResponse, status_code=201, responses={
    201: {"description": "Proveedor creado"},
    400: {"description": "Error de petición"},
    422: {"description": "Error de validación"}
})
def create(data: ProveedorCreate, db: Session = Depends(get_db)):
    service = get_ProveedorService()(db)
    return service.crear(data)

@router.put("/{id}", response_model=ProveedorResponse, responses={
    200: {"description": "Proveedor actualizado"},
    400: {"description": "Error de petición"},
    404: {"description": "Proveedor no encontrado"},
    422: {"description": "Error de validación"}
})
def update(id: int, data: ProveedorUpdate, db: Session = Depends(get_db)):
    service = get_ProveedorService()(db)
    result = service.actualizar(id, data)
    return result

@router.delete("/{id}", responses={
    200: {"description": "Proveedor eliminado"},
    400: {"description": "Error de petición"},
    404: {"description": "Proveedor no encontrado"},
    422: {"description": "Error de validación"}
})
def delete(id: int, db: Session = Depends(get_db)):
    service = get_ProveedorService()(db)
    return service.eliminar(id)
