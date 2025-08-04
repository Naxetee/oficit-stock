from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.familia_schema import FamiliaResponse, FamiliaCreate, FamiliaUpdate
from ..services import get_FamiliaService
from app.db import get_db

router = APIRouter(prefix="/familia", tags=["Familia"])

@router.get("/", response_model=list[FamiliaResponse], responses={
    200: {"description": "Lista de familias"},
    422: {"description": "Error de validación"}
})
def get_all(db: Session = Depends(get_db)):
    service = get_FamiliaService()(db)
    return service.obtener_todos()

@router.get("/{id}", response_model=FamiliaResponse, responses={
    200: {"description": "Familia encontrada"},
    404: {"description": "Familia no encontrada"},
    422: {"description": "Error de validación"}
})
def get_by_id(id: int, db: Session = Depends(get_db)):
    service = get_FamiliaService()(db)
    result = service.obtener_por_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Familia no encontrada")
    return result

@router.post("/", response_model=FamiliaResponse, responses={
    201: {"description": "Familia creada"},
    422: {"description": "Error de validación"}
})
def create(data: FamiliaCreate, db: Session = Depends(get_db)):
    service = get_FamiliaService()(db)
    return service.crear(data)

@router.put("/{id}", response_model=FamiliaResponse, responses={
    200: {"description": "Familia actualizada"},
    404: {"description": "Familia no encontrada"},
    422: {"description": "Error de validación"}
})
def update(id: int, data: FamiliaUpdate, db: Session = Depends(get_db)):
    service = get_FamiliaService()(db)
    result = service.actualizar(id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Familia no encontrada")
    return result

@router.delete("/{id}", responses={
    200: {"description": "Familia eliminada"},
    404: {"description": "Familia no encontrada"},
    422: {"description": "Error de validación"}
})
def delete(id: int, db: Session = Depends(get_db)):
    service = get_FamiliaService()(db)
    return service.eliminar(id)
