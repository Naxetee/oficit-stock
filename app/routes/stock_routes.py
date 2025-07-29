"""
📊 Rutas para el modelo Stock

Endpoints RESTful para gestionar el stock de productos y componentes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import SessionLocal
from app.services.stock_service import StockService

router = APIRouter(prefix="/stock", tags=["Stock"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/producto/{producto_simple_id}", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_stock_producto(
    producto_simple_id: int,
    cantidad_actual: float,
    cantidad_minima: Optional[float] = None,
    cantidad_maxima: Optional[float] = None,
    ubicacion_almacen: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """🆕 Crear registro de stock para producto simple"""
    try:
        stock_service = StockService(db)
        stock = stock_service.crear_stock_producto(
            producto_simple_id=producto_simple_id,
            cantidad_actual=cantidad_actual,
            cantidad_minima=cantidad_minima,
            cantidad_maxima=cantidad_maxima,
            ubicacion_almacen=ubicacion_almacen
        )
        return {
            "mensaje": "Stock de producto creado exitosamente",
            "stock": {
                "id": stock.id,
                "cantidad_actual": float(stock.cantidad_actual),
                "cantidad_minima": float(stock.cantidad_minima) if stock.cantidad_minima else None,
                "cantidad_maxima": float(stock.cantidad_maxima) if stock.cantidad_maxima else None,
                "ubicacion_almacen": stock.ubicacion_almacen,
                "id_producto_simple": stock.id_producto_simple
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear stock: {str(e)}")

@router.post("/componente/{componente_id}", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_stock_componente(
    componente_id: int,
    cantidad_actual: float,
    cantidad_minima: Optional[float] = None,
    cantidad_maxima: Optional[float] = None,
    ubicacion_almacen: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """🆕 Crear registro de stock para componente"""
    try:
        stock_service = StockService(db)
        stock = stock_service.crear_stock_componente(
            componente_id=componente_id,
            cantidad_actual=cantidad_actual,
            cantidad_minima=cantidad_minima,
            cantidad_maxima=cantidad_maxima,
            ubicacion_almacen=ubicacion_almacen
        )
        return {
            "mensaje": "Stock de componente creado exitosamente",
            "stock": {
                "id": stock.id,
                "cantidad_actual": float(stock.cantidad_actual),
                "cantidad_minima": float(stock.cantidad_minima) if stock.cantidad_minima else None,
                "cantidad_maxima": float(stock.cantidad_maxima) if stock.cantidad_maxima else None,
                "ubicacion_almacen": stock.ubicacion_almacen,
                "id_componente": stock.id_componente
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear stock: {str(e)}")

@router.get("/", response_model=List[dict])
def listar_stock(
    bajo_minimo: Optional[bool] = None,
    ubicacion: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """📋 Obtener lista de registros de stock con filtros opcionales"""
    try:
        stock_service = StockService(db)
        stocks = stock_service.listar_stock(
            bajo_minimo=bajo_minimo,
            ubicacion=ubicacion,
            skip=skip,
            limit=limit
        )
        return [
            {
                "id": stock.id,
                "cantidad_actual": float(stock.cantidad_actual),
                "cantidad_minima": float(stock.cantidad_minima) if stock.cantidad_minima else None,
                "cantidad_maxima": float(stock.cantidad_maxima) if stock.cantidad_maxima else None,
                "ubicacion_almacen": stock.ubicacion_almacen,
                "id_producto_simple": stock.id_producto_simple,
                "id_componente": stock.id_componente,
                "created_at": stock.created_at,
                "updated_at": stock.updated_at
            }
            for stock in stocks
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al listar stock: {str(e)}")

@router.get("/{stock_id}", response_model=dict)
def obtener_stock(stock_id: int, db: Session = Depends(get_db)):
    """🔍 Obtener un registro de stock específico por ID"""
    try:
        stock_service = StockService(db)
        stock = stock_service.obtener_stock(stock_id)
        if not stock:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock no encontrado")
        return {
            "id": stock.id,
            "cantidad_actual": float(stock.cantidad_actual),
            "cantidad_minima": float(stock.cantidad_minima) if stock.cantidad_minima else None,
            "cantidad_maxima": float(stock.cantidad_maxima) if stock.cantidad_maxima else None,
            "ubicacion_almacen": stock.ubicacion_almacen,
            "id_producto_simple": stock.id_producto_simple,
            "id_componente": stock.id_componente,
            "created_at": stock.created_at,
            "updated_at": stock.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener stock: {str(e)}")

@router.put("/{stock_id}/cantidad", response_model=dict)
def actualizar_cantidad_stock(
    stock_id: int,
    nueva_cantidad: float,
    db: Session = Depends(get_db)
):
    """✏️ Actualizar cantidad actual de stock"""
    try:
        stock_service = StockService(db)
        stock = stock_service.actualizar_cantidad(stock_id, nueva_cantidad)
        if not stock:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock no encontrado")
        return {
            "mensaje": "Cantidad de stock actualizada exitosamente",
            "stock": {
                "id": stock.id,
                "cantidad_actual": float(stock.cantidad_actual)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al actualizar stock: {str(e)}")

@router.post("/{stock_id}/movimiento", response_model=dict)
def registrar_movimiento_stock(
    stock_id: int,
    cantidad: float,
    tipo_movimiento: str,  # "entrada" o "salida"
    motivo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """📝 Registrar movimiento de stock (entrada/salida)"""
    try:
        stock_service = StockService(db)
        if tipo_movimiento not in ["entrada", "salida"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de movimiento debe ser 'entrada' o 'salida'")
        
        stock = stock_service.registrar_movimiento(stock_id, cantidad, tipo_movimiento, motivo)
        return {
            "mensaje": f"Movimiento de {tipo_movimiento} registrado exitosamente",
            "stock": {
                "id": stock.id,
                "cantidad_actual": float(stock.cantidad_actual)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al registrar movimiento: {str(e)}")

@router.get("/alertas/bajo-minimo", response_model=List[dict])
def obtener_alertas_stock_bajo(db: Session = Depends(get_db)):
    """⚠️ Obtener elementos con stock por debajo del mínimo"""
    try:
        stock_service = StockService(db)
        alertas = stock_service.obtener_stock_bajo_minimo()
        return [
            {
                "id": stock.id,
                "cantidad_actual": float(stock.cantidad_actual),
                "cantidad_minima": float(stock.cantidad_minima),
                "diferencia": float(stock.cantidad_minima - stock.cantidad_actual),
                "ubicacion_almacen": stock.ubicacion_almacen,
                "tipo": "producto" if stock.id_producto_simple else "componente",
                "elemento_id": stock.id_producto_simple if stock.id_producto_simple else stock.id_componente
            }
            for stock in alertas
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener alertas: {str(e)}")
