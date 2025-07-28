from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Text, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class PrecioVenta(Base):
    """
    💰 Precio_Venta - Registra los precios de venta de los artículos
    
    Esta clase mantiene un histórico de precios de venta, permitiendo
    gestionar cambios de precios de forma controlada y trazable.
    
    Attributes:
        id (int): Identificador único del precio
        valor (Decimal): Precio de venta del artículo
        moneda (str): Código de moneda (EUR, USD, etc.)
        fecha_inicio (datetime): Fecha de inicio de validez del precio
        fecha_fin (datetime): Fecha de fin de validez (None si está activo)
        created_at (datetime): Fecha y hora de creación
        updated_at (datetime): Fecha y hora de última actualización
        
    Relationships:
        articulos (List[Articulo]): Artículos que usan este precio
    """
    __tablename__ = "precio_venta"
    
    # Restricciones de integridad
    __table_args__ = (
        CheckConstraint("valor > 0", name='check_precio_venta_positivo'),
        CheckConstraint("fecha_fin IS NULL OR fecha_fin > fecha_inicio", name='check_fechas_venta_logicas'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Numeric(10, 2), nullable=False)
    moneda = Column(String(3), default='EUR')  # EUR, USD, etc.
    fecha_inicio = Column(DateTime(timezone=True), server_default=func.now())
    fecha_fin = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    articulos = relationship("Articulo", back_populates="precio_venta")
    
    def __repr__(self):
        return f"<PrecioVenta(id={self.id}, precio={self.valor} {self.moneda})>"
