"""
💰 Rutas para los modelos de Precios

Endpoints RESTful para gestionar precios de compra y venta.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from app.db import SessionLocal
from app.services.precio_service import PrecioService

router = APIRouter(prefix="/precios", tags=["Precios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# ENDPOINTS PARA PRECIOS DE COMPRA
# ==========================================

@router.post("/compra", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_precio_compra(
    valor: float,
    moneda: str = "EUR",
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    🆕 Crear un nuevo precio de compra
    """
    try:
        precio_service = PrecioService(db)
        precio = precio_service.crear_precio_compra(
            valor=Decimal(str(valor)),
            moneda=moneda,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        return {
            "mensaje": "Precio de compra creado exitosamente",
            "precio_compra": {
                "id": precio.id,
                "valor": float(precio.valor),
                "moneda": precio.moneda,
                "fecha_inicio": precio.fecha_inicio,
                "fecha_fin": precio.fecha_fin
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear precio de compra: {str(e)}"
        )

@router.get("/compra", response_model=List[dict])
def listar_precios_compra(
    vigente: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    📋 Obtener lista de precios de compra
    """
    try:
        precio_service = PrecioService(db)
        precios = precio_service.listar_precios_compra(
            vigente=vigente,
            skip=skip,
            limit=limit
        )
        return [
            {
                "id": precio.id,
                "valor": float(precio.valor),
                "moneda": precio.moneda,
                "fecha_inicio": precio.fecha_inicio,
                "fecha_fin": precio.fecha_fin,
                "created_at": precio.created_at,
                "updated_at": precio.updated_at
            }
            for precio in precios
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar precios de compra: {str(e)}"
        )

@router.get("/compra/{precio_id}", response_model=dict)
def obtener_precio_compra(
    precio_id: int,
    db: Session = Depends(get_db)
):
    """
    🔍 Obtener un precio de compra específico por ID
    """
    try:
        precio_service = PrecioService(db)
        precio = precio_service.obtener_precio_compra(precio_id)
        if not precio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Precio de compra no encontrado"
            )
        return {
            "id": precio.id,
            "valor": float(precio.valor),
            "moneda": precio.moneda,
            "fecha_inicio": precio.fecha_inicio,
            "fecha_fin": precio.fecha_fin,
            "created_at": precio.created_at,
            "updated_at": precio.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener precio de compra: {str(e)}"
        )

# ==========================================
# ENDPOINTS PARA PRECIOS DE VENTA
# ==========================================

@router.post("/venta", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_precio_venta(
    valor: float,
    moneda: str = "EUR",
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    🆕 Crear un nuevo precio de venta
    """
    try:
        precio_service = PrecioService(db)
        precio = precio_service.crear_precio_venta(
            valor=Decimal(str(valor)),
            moneda=moneda,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        return {
            "mensaje": "Precio de venta creado exitosamente",
            "precio_venta": {
                "id": precio.id,
                "valor": float(precio.valor),
                "moneda": precio.moneda,
                "fecha_inicio": precio.fecha_inicio,
                "fecha_fin": precio.fecha_fin
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear precio de venta: {str(e)}"
        )

@router.get("/venta", response_model=List[dict])
def listar_precios_venta(
    vigente: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    📋 Obtener lista de precios de venta
    """
    try:
        precio_service = PrecioService(db)
        precios = precio_service.listar_precios_venta(
            vigente=vigente,
            skip=skip,
            limit=limit
        )
        return [
            {
                "id": precio.id,
                "valor": float(precio.valor),
                "moneda": precio.moneda,
                "fecha_inicio": precio.fecha_inicio,
                "fecha_fin": precio.fecha_fin,
                "created_at": precio.created_at,
                "updated_at": precio.updated_at
            }
            for precio in precios
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar precios de venta: {str(e)}"
        )

@router.get("/venta/{precio_id}", response_model=dict)
def obtener_precio_venta(
    precio_id: int,
    db: Session = Depends(get_db)
):
    """
    🔍 Obtener un precio de venta específico por ID
    """
    try:
        precio_service = PrecioService(db)
        precio = precio_service.obtener_precio_venta(precio_id)
        if not precio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Precio de venta no encontrado"
            )
        return {
            "id": precio.id,
            "valor": float(precio.valor),
            "moneda": precio.moneda,
            "fecha_inicio": precio.fecha_inicio,
            "fecha_fin": precio.fecha_fin,
            "created_at": precio.created_at,
            "updated_at": precio.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener precio de venta: {str(e)}"
        )

# ==========================================
# ENDPOINTS ESPECIALIZADOS
# ==========================================

@router.put("/compra/{precio_id}", response_model=dict)
def actualizar_precio_compra(
    precio_id: int,
    valor: Optional[float] = None,
    moneda: Optional[str] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    ✏️ Actualizar un precio de compra existente
    """
    try:
        precio_service = PrecioService(db)
        precio = precio_service.actualizar_precio_compra(
            precio_id=precio_id,
            valor=Decimal(str(valor)) if valor else None,
            moneda=moneda,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        if not precio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Precio de compra no encontrado"
            )
        return {
            "mensaje": "Precio de compra actualizado exitosamente",
            "precio_compra": {
                "id": precio.id,
                "valor": float(precio.valor),
                "moneda": precio.moneda,
                "fecha_inicio": precio.fecha_inicio,
                "fecha_fin": precio.fecha_fin
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar precio de compra: {str(e)}"
        )

@router.put("/venta/{precio_id}", response_model=dict)
def actualizar_precio_venta(
    precio_id: int,
    valor: Optional[float] = None,
    moneda: Optional[str] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    ✏️ Actualizar un precio de venta existente
    """
    try:
        precio_service = PrecioService(db)
        precio = precio_service.actualizar_precio_venta(
            precio_id=precio_id,
            valor=Decimal(str(valor)) if valor else None,
            moneda=moneda,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        if not precio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Precio de venta no encontrado"
            )
        return {
            "mensaje": "Precio de venta actualizado exitosamente",
            "precio_venta": {
                "id": precio.id,
                "valor": float(precio.valor),
                "moneda": precio.moneda,
                "fecha_inicio": precio.fecha_inicio,
                "fecha_fin": precio.fecha_fin
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar precio de venta: {str(e)}"
        )
