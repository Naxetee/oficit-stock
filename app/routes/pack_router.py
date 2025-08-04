from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.pack_schema import PackResponse, PackCreate, PackUpdate
from ..services import get_PackService
from ..db import get_db

router = APIRouter(prefix="/pack", tags=["Pack"])

@router.get("/", response_model=list[PackResponse], responses={
    200: {"description": "Lista de packs"},
    422: {"description": "Error de validación"}
})
def get_all(db: Session = Depends(get_db)):
    service = get_PackService()(db)
    return service.obtener_todos()

@router.get("/{id}", response_model=PackResponse, responses={
    200: {"description": "Pack encontrado"},
    404: {"description": "Pack no encontrado"},
    422: {"description": "Error de validación"}
})
def get_by_id(id: int, db: Session = Depends(get_db)):
    service = get_PackService()(db)
    result = service.obtener_por_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return result

@router.post("/", response_model=PackResponse, responses={
    201: {"description": "Pack creado"},
    422: {"description": "Error de validación"}
})
def create(data: PackCreate, db: Session = Depends(get_db)):
    service = get_PackService()(db)
    return service.crear(data)

@router.put("/{id}", response_model=PackResponse, responses={
    200: {"description": "Pack actualizado"},
    404: {"description": "Pack no encontrado"},
    422: {"description": "Error de validación"}
})
def update(id: int, data: PackUpdate, db: Session = Depends(get_db)):
    service = get_PackService()(db)
    result = service.actualizar(id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return result

@router.delete("/{id}", responses={
    200: {"description": "Pack eliminado"},
    404: {"description": "Pack no encontrado"},
    422: {"description": "Error de validación"}
})
def delete(id: int, db: Session = Depends(get_db)):
    service = get_PackService()(db)
    return service.eliminar(id)
