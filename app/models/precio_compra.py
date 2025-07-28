from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class PrecioCompra(Base):
    """
    🛒 Precio_Compra - Registra los precios de compra de productos simples y componentes
    
    Esta clase mantiene un histórico de precios de compra para calcular
    costos y márgenes de beneficio de forma precisa.
    
    Attributes:
        id (int): Identificador único del precio
        valor (Decimal): Precio de compra
        moneda (str): Código de moneda (EUR, USD, etc.)
        fecha_inicio (datetime): Fecha de inicio de validez del precio
        fecha_fin (datetime): Fecha de fin de validez (None si está activo)
        created_at (datetime): Fecha y hora de creación
        updated_at (datetime): Fecha y hora de última actualización
        
    Relationships:
        productos_simples (List[ProductoSimple]): Productos con este precio
        componentes (List[Componente]): Componentes con este precio
    """
    __tablename__ = "precio_compra"
    
    # Restricciones de integridad
    __table_args__ = (
        CheckConstraint("valor > 0", name='check_precio_compra_positivo'),
        CheckConstraint("fecha_fin IS NULL OR fecha_fin > fecha_inicio", name='check_fechas_compra_logicas'),
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
    productos_simples = relationship("ProductoSimple", back_populates="precio_compra")
    componentes = relationship("Componente", back_populates="precio_compra")
    
    def __repr__(self):
        return f"<PrecioCompra(id={self.id}, precio={self.valor} {self.moneda})>"
