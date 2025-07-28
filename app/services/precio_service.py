"""
💰 Servicio de Precios - Gestión de precios de venta y compra

Este servicio maneja todas las operaciones relacionadas con los precios
de venta y compra, incluyendo históricos y validaciones de fechas.
"""

from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_

from app.models.precio_venta import PrecioVenta
from app.models.precio_compra import PrecioCompra
from app.models.articulo import Articulo
from app.models.producto_simple import ProductoSimple
from app.models.componente import Componente
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class PrecioService:
    """
    💰 Servicio para gestión de precios de venta y compra
    
    Maneja operaciones específicas de precios incluyendo:
    - CRUD de precios de venta y compra
    - Gestión de históricos de precios
    - Validaciones de fechas y montos
    - Consultas de precios activos y por períodos
    """
    
    def __init__(self, db_session: Session):
        """
        Constructor del servicio de precios
        
        Args:
            db_session (Session): Sesión de base de datos SQLAlchemy
        """
        self.db = db_session
        
    # =================== PRECIOS DE VENTA ===================
        
    def crear_precio_venta(self, valor: float, moneda: str = 'EUR',
                          fecha_inicio: datetime = None, fecha_fin: datetime = None) -> PrecioVenta:
        """
        Crear un nuevo precio de venta
        
        Args:
            valor (float): Valor del precio (debe ser positivo)
            moneda (str, optional): Código de moneda (default: 'EUR')
            fecha_inicio (datetime, optional): Fecha de inicio (default: ahora)
            fecha_fin (datetime, optional): Fecha de fin (default: None)
            
        Returns:
            PrecioVenta: Nuevo precio de venta creado
            
        Raises:
            ValueError: Si hay errores de validación
            SQLAlchemyError: Error en la operación de base de datos
        """
        try:
            if valor <= 0:
                raise ValueError("El valor del precio debe ser positivo")
                
            if fecha_fin and fecha_inicio and fecha_fin <= fecha_inicio:
                raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
                
            precio_venta = PrecioVenta(
                valor=Decimal(valor),
                moneda=moneda,
                fecha_inicio=fecha_inicio or datetime.now(),
                fecha_fin=fecha_fin
            )
            
            self.db.add(precio_venta)
            self.db.commit()
            self.db.refresh(precio_venta)
            
            logger.info(f"✅ Precio de venta {valor} {moneda} creado exitosamente")
            return precio_venta
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error creando precio de venta: {e}")
            raise
            
    def obtener_precio_venta_activo(self, precio_id: int) -> Optional[PrecioVenta]:
        """
        Obtener un precio de venta que esté activo (sin fecha_fin o fecha_fin futura)
        
        Args:
            precio_id (int): ID del precio de venta
            
        Returns:
            Optional[PrecioVenta]: Precio activo o None
        """
        try:
            return self.db.query(PrecioVenta).filter(
                and_(
                    PrecioVenta.id == precio_id,
                    or_(
                        PrecioVenta.fecha_fin.is_(None),
                        PrecioVenta.fecha_fin > datetime.now()
                    )
                )
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo precio de venta activo {precio_id}: {e}")
            raise
            
    def obtener_articulos_con_precio_venta(self, precio_id: int) -> List[Articulo]:
        """
        Obtener todos los artículos que usan un precio de venta específico
        
        Args:
            precio_id (int): ID del precio de venta
            
        Returns:
            List[Articulo]: Lista de artículos con el precio
        """
        try:
            return self.db.query(Articulo).filter(
                Articulo.id_precio_venta == precio_id
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo artículos con precio {precio_id}: {e}")
            raise
            
    def finalizar_precio_venta(self, precio_id: int, fecha_fin: datetime = None) -> Optional[PrecioVenta]:
        """
        Finalizar un precio de venta estableciendo su fecha de fin
        
        Args:
            precio_id (int): ID del precio de venta
            fecha_fin (datetime, optional): Fecha de fin (default: ahora)
            
        Returns:
            Optional[PrecioVenta]: Precio actualizado o None si no existe
        """
        try:
            precio = self.db.query(PrecioVenta).filter(PrecioVenta.id == precio_id).first()
            if not precio:
                return None
                
            precio.fecha_fin = fecha_fin or datetime.now()
            self.db.commit()
            self.db.refresh(precio)
            
            logger.info(f"✅ Precio de venta {precio_id} finalizado")
            return precio
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error finalizando precio de venta {precio_id}: {e}")
            raise
            
    # =================== PRECIOS DE COMPRA ===================
        
    def crear_precio_compra(self, valor: float, moneda: str = 'EUR',
                           fecha_inicio: datetime = None, fecha_fin: datetime = None) -> PrecioCompra:
        """
        Crear un nuevo precio de compra
        
        Args:
            valor (float): Valor del precio (debe ser positivo)
            moneda (str, optional): Código de moneda (default: 'EUR')
            fecha_inicio (datetime, optional): Fecha de inicio (default: ahora)
            fecha_fin (datetime, optional): Fecha de fin (default: None)
            
        Returns:
            PrecioCompra: Nuevo precio de compra creado
            
        Raises:
            ValueError: Si hay errores de validación
            SQLAlchemyError: Error en la operación de base de datos
        """
        try:
            if valor <= 0:
                raise ValueError("El valor del precio debe ser positivo")
                
            if fecha_fin and fecha_inicio and fecha_fin <= fecha_inicio:
                raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
                
            precio_compra = PrecioCompra(
                valor=Decimal(valor),
                moneda=moneda,
                fecha_inicio=fecha_inicio or datetime.now(),
                fecha_fin=fecha_fin
            )
            
            self.db.add(precio_compra)
            self.db.commit()
            self.db.refresh(precio_compra)
            
            logger.info(f"✅ Precio de compra {valor} {moneda} creado exitosamente")
            return precio_compra
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error creando precio de compra: {e}")
            raise
            
    def obtener_precio_compra_activo(self, precio_id: int) -> Optional[PrecioCompra]:
        """
        Obtener un precio de compra que esté activo
        
        Args:
            precio_id (int): ID del precio de compra
            
        Returns:
            Optional[PrecioCompra]: Precio activo o None
        """
        try:
            return self.db.query(PrecioCompra).filter(
                and_(
                    PrecioCompra.id == precio_id,
                    or_(
                        PrecioCompra.fecha_fin.is_(None),
                        PrecioCompra.fecha_fin > datetime.now()
                    )
                )
            ).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo precio de compra activo {precio_id}: {e}")
            raise
            
    def obtener_productos_con_precio_compra(self, precio_id: int) -> List[ProductoSimple]:
        """
        Obtener todos los productos simples que usan un precio de compra específico
        
        Args:
            precio_id (int): ID del precio de compra
            
        Returns:
            List[ProductoSimple]: Lista de productos con el precio
        """
        try:
            return self.db.query(ProductoSimple).filter(
                ProductoSimple.id_precio_compra == precio_id
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo productos con precio compra {precio_id}: {e}")
            raise
            
    def obtener_componentes_con_precio_compra(self, precio_id: int) -> List[Componente]:
        """
        Obtener todos los componentes que usan un precio de compra específico
        
        Args:
            precio_id (int): ID del precio de compra
            
        Returns:
            List[Componente]: Lista de componentes con el precio
        """
        try:
            return self.db.query(Componente).filter(
                Componente.id_precio_compra == precio_id
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo componentes con precio compra {precio_id}: {e}")
            raise
            
    # =================== CONSULTAS GENERALES ===================
    
    def obtener_historico_precios_venta(self, moneda: str = None, 
                                       fecha_desde: date = None, 
                                       fecha_hasta: date = None) -> List[PrecioVenta]:
        """
        Obtener histórico de precios de venta con filtros opcionales
        
        Args:
            moneda (str, optional): Filtrar por moneda
            fecha_desde (date, optional): Fecha de inicio del rango
            fecha_hasta (date, optional): Fecha de fin del rango
            
        Returns:
            List[PrecioVenta]: Lista de precios de venta
        """
        try:
            query = self.db.query(PrecioVenta)
            
            if moneda:
                query = query.filter(PrecioVenta.moneda == moneda)
                
            if fecha_desde:
                query = query.filter(PrecioVenta.fecha_inicio >= fecha_desde)
                
            if fecha_hasta:
                query = query.filter(
                    or_(
                        PrecioVenta.fecha_fin.is_(None),
                        PrecioVenta.fecha_fin <= fecha_hasta
                    )
                )
                
            return query.order_by(PrecioVenta.fecha_inicio.desc()).all()
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo histórico de precios de venta: {e}")
            raise
            
    def obtener_historico_precios_compra(self, moneda: str = None,
                                        fecha_desde: date = None,
                                        fecha_hasta: date = None) -> List[PrecioCompra]:
        """
        Obtener histórico de precios de compra con filtros opcionales
        
        Args:
            moneda (str, optional): Filtrar por moneda
            fecha_desde (date, optional): Fecha de inicio del rango
            fecha_hasta (date, optional): Fecha de fin del rango
            
        Returns:
            List[PrecioCompra]: Lista de precios de compra
        """
        try:
            query = self.db.query(PrecioCompra)
            
            if moneda:
                query = query.filter(PrecioCompra.moneda == moneda)
                
            if fecha_desde:
                query = query.filter(PrecioCompra.fecha_inicio >= fecha_desde)
                
            if fecha_hasta:
                query = query.filter(
                    or_(
                        PrecioCompra.fecha_fin.is_(None),
                        PrecioCompra.fecha_fin <= fecha_hasta
                    )
                )
                
            return query.order_by(PrecioCompra.fecha_inicio.desc()).all()
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo histórico de precios de compra: {e}")
            raise
            
    def calcular_margen_beneficio(self, precio_venta_id: int, precio_compra_id: int) -> dict:
        """
        Calcular el margen de beneficio entre un precio de venta y compra
        
        Args:
            precio_venta_id (int): ID del precio de venta
            precio_compra_id (int): ID del precio de compra
            
        Returns:
            dict: Información del margen incluyendo:
                - margen_absoluto: Diferencia en valor absoluto
                - margen_porcentual: Porcentaje de margen
                - precio_venta: Valor de venta
                - precio_compra: Valor de compra
        """
        try:
            precio_venta = self.db.query(PrecioVenta).filter(PrecioVenta.id == precio_venta_id).first()
            precio_compra = self.db.query(PrecioCompra).filter(PrecioCompra.id == precio_compra_id).first()
            
            if not precio_venta or not precio_compra:
                return {'error': 'Uno o ambos precios no existen'}
                
            if precio_venta.moneda != precio_compra.moneda:
                return {'error': 'Los precios deben estar en la misma moneda'}
                
            margen_absoluto = precio_venta.valor - precio_compra.valor
            margen_porcentual = (margen_absoluto / precio_compra.valor) * 100 if precio_compra.valor > 0 else 0
            
            return {
                'precio_venta': float(precio_venta.valor),
                'precio_compra': float(precio_compra.valor),
                'margen_absoluto': float(margen_absoluto),
                'margen_porcentual': float(margen_porcentual),
                'moneda': precio_venta.moneda
            }
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error calculando margen de beneficio: {e}")
            raise
