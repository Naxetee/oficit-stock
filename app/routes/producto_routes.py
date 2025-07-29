"""
🏷️ Rutas para el modelo Producto

Endpoints RESTful para gestionar productos (simples y compuestos).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
from app.services.producto_service import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/simple", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_producto_simple(
    id_articulo: int,
    especificaciones: Optional[str] = None,
    id_proveedor: Optional[int] = None,
    id_precio_compra: Optional[int] = None,
    id_color: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """🆕 Crear un nuevo producto simple"""
    try:
        producto_service = ProductoService(db)
        producto = producto_service.crear_producto_simple(
            id_articulo=id_articulo,
            especificaciones=especificaciones,
            id_proveedor=id_proveedor,
            id_precio_compra=id_precio_compra,
            id_color=id_color
        )
        return {
            "mensaje": "Producto simple creado exitosamente",
            "producto": {
                "id": producto.id,
                "tipo_producto": "simple",
                "id_articulo": producto.id_articulo
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear producto simple: {str(e)}")

@router.post("/compuesto", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_producto_compuesto(
    id_articulo: int,
    db: Session = Depends(get_db)
):
    """🆕 Crear un nuevo producto compuesto"""
    try:
        producto_service = ProductoService(db)
        producto = producto_service.crear_producto_compuesto(id_articulo=id_articulo)
        return {
            "mensaje": "Producto compuesto creado exitosamente",
            "producto": {
                "id": producto.id,
                "tipo_producto": "compuesto",
                "id_articulo": producto.id_articulo
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear producto compuesto: {str(e)}")

@router.get("/", response_model=List[dict])
def listar_productos(
    tipo_producto: Optional[str] = None,
    id_articulo: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """📋 Obtener lista de productos con filtros opcionales"""
    try:
        producto_service = ProductoService(db)
        productos = producto_service.listar_productos(
            tipo_producto=tipo_producto,
            id_articulo=id_articulo,
            skip=skip,
            limit=limit
        )
        return [
            {
                "id": producto.id,
                "tipo_producto": producto.tipo_producto,
                "id_articulo": producto.id_articulo,
                "created_at": producto.created_at,
                "updated_at": producto.updated_at
            }
            for producto in productos
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al listar productos: {str(e)}")

@router.get("/{producto_id}", response_model=dict)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    """🔍 Obtener un producto específico por ID"""
    try:
        producto_service = ProductoService(db)
        producto = producto_service.obtener_producto(producto_id)
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return {
            "id": producto.id,
            "tipo_producto": producto.tipo_producto,
            "id_articulo": producto.id_articulo,
            "created_at": producto.created_at,
            "updated_at": producto.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener producto: {str(e)}")

@router.delete("/{producto_id}", response_model=dict)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    """🗑️ Eliminar un producto"""
    try:
        producto_service = ProductoService(db)
        success = producto_service.eliminar_producto(producto_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return {"mensaje": "Producto eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al eliminar producto: {str(e)}")

@router.get("/{producto_id}/componentes", response_model=List[dict])
def obtener_componentes_producto(producto_id: int, db: Session = Depends(get_db)):
    """🔧 Obtener componentes de un producto compuesto"""
    try:
        producto_service = ProductoService(db)
        componentes = producto_service.obtener_componentes_producto(producto_id)
        return [
            {
                "id": rel.id,
                "cantidad_necesaria": float(rel.cantidad_necesaria),
                "componente": {
                    "id": rel.componente.id,
                    "nombre": rel.componente.nombre,
                    "codigo": rel.componente.codigo
                }
            }
            for rel in componentes
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener componentes: {str(e)}")

@router.post("/{producto_id}/componentes/{componente_id}", response_model=dict)
def agregar_componente_a_producto(
    producto_id: int,
    componente_id: int,
    cantidad_necesaria: float,
    db: Session = Depends(get_db)
):
    """➕ Agregar componente a producto compuesto"""
    try:
        producto_service = ProductoService(db)
        relacion = producto_service.agregar_componente_a_producto(producto_id, componente_id, cantidad_necesaria)
        return {
            "mensaje": "Componente agregado al producto exitosamente",
            "relacion": {
                "id": relacion.id,
                "cantidad_necesaria": float(relacion.cantidad_necesaria)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al agregar componente: {str(e)}")
