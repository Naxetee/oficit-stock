from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.color_schema import ColorResponse, ColorCreate, ColorUpdate
from ..services import get_ColorService
from ..db import get_db

router = APIRouter(prefix="/color", tags=["Color"])

@router.get("/", response_model=list[ColorResponse], responses={
    200: {"description": "Lista de colores"},
    422: {"description": "Error de validación"}
})
def get_all(db: Session = Depends(get_db)):
    service = get_ColorService()(db)
    return service.obtener_todos()

@router.get("/{id}", response_model=ColorResponse, responses={
    200: {"description": "Color encontrado"},
    404: {"description": "Color no encontrado"},
    422: {"description": "Error de validación"}
})
def get_by_id(id: int, db: Session = Depends(get_db)):
    service = get_ColorService()(db)
    result = service.obtener_por_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Color no encontrado")
    return result

@router.post("/", response_model=ColorResponse, responses={
    201: {"description": "Color creado"},
    422: {"description": "Error de validación"}
})
def create(data: ColorCreate, db: Session = Depends(get_db)):
    service = get_ColorService()(db)
    return service.crear(data)

@router.put("/{id}", response_model=ColorResponse, responses={
    200: {"description": "Color actualizado"},
    404: {"description": "Color no encontrado"},
    422: {"description": "Error de validación"}
})
def update(id: int, data: ColorUpdate, db: Session = Depends(get_db)):
    service = get_ColorService()(db)
    result = service.actualizar(id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Color no encontrado")
    return result

@router.delete("/{id}", responses={
    200: {"description": "Color eliminado"},
    404: {"description": "Color no encontrado"},
    422: {"description": "Error de validación"}
})
def delete(id: int, db: Session = Depends(get_db)):
    service = get_ColorService()(db)
    return service.eliminar(id)
