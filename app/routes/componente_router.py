from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.componente_schema import ComponenteResponse, ComponenteCreate, ComponenteUpdate
from ..services import get_ComponenteService
from ..db import get_db

router = APIRouter(prefix="/componente", tags=["Componente"])

@router.get("/", response_model=list[ComponenteResponse], responses={
    200: {"description": "Lista de componentes"},
    422: {"description": "Error de validación"}
})
def get_all(db: Session = Depends(get_db)):
    service = get_ComponenteService()(db)
    return service.obtener_todos()

@router.get("/{id}", response_model=ComponenteResponse, responses={
    200: {"description": "Componente encontrado"},
    404: {"description": "Componente no encontrado"},
    422: {"description": "Error de validación"}
})
def get_by_id(id: int, db: Session = Depends(get_db)):
    service = get_ComponenteService()(db)
    result = service.obtener_por_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    return result

@router.post("/", response_model=ComponenteResponse, responses={
    201: {"description": "Componente creado"},
    422: {"description": "Error de validación"}
})
def create(data: ComponenteCreate, db: Session = Depends(get_db)):
    service = get_ComponenteService()(db)
    return service.crear(data)

@router.put("/{id}", response_model=ComponenteResponse, responses={
    200: {"description": "Componente actualizado"},
    404: {"description": "Componente no encontrado"},
    422: {"description": "Error de validación"}
})
def update(id: int, data: ComponenteUpdate, db: Session = Depends(get_db)):
    service = get_ComponenteService()(db)
    result = service.actualizar(id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    return result

@router.delete("/{id}", responses={
    200: {"description": "Componente eliminado"},
    404: {"description": "Componente no encontrado"},
    422: {"description": "Error de validación"}
})
def delete(id: int, db: Session = Depends(get_db)):
    service = get_ComponenteService()(db)
    return service.eliminar(id)
