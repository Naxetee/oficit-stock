from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, CheckConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Stock(Base):
    """
    🏬 Stock - Registra la cantidad disponible de productos simples y componentes en el almacén
    
    Controla el inventario físico de productos simples y componentes,
    gestionando cantidades, ubicaciones y alertas de reposición.
    
    Attributes:
        id (int): Identificador único del registro de stock
        cantidad_actual (Decimal): Cantidad disponible actualmente
        cantidad_minima (Decimal): Nivel mínimo antes de alerta
        cantidad_maxima (Decimal): Nivel máximo recomendado
        ubicacion_almacen (str): Ubicación física en el almacén
        id_producto_simple (int): Ref. a producto simple (exclusivo con componente)
        id_componente (int): Ref. a componente (exclusivo con producto simple)
        created_at (datetime): Fecha y hora de creación
        updated_at (datetime): Fecha y hora de última actualización
        
    Relationships:
        producto_simple (ProductoSimple): Producto simple asociado (si aplica)
        componente (Componente): Componente asociado (si aplica)
        
    Properties:
        elemento: Elemento asociado (producto simple o componente)
        nombre_elemento: Nombre del elemento en stock
        necesita_reposicion: True si está por debajo del mínimo
    """
    __tablename__ = "stock"
    
    # Restricciones a nivel de base de datos para relación exclusiva
    __table_args__ = (
        CheckConstraint(
            text("id_producto_simple IS NOT NULL AND id_componente IS NULL OR id_producto_simple IS NULL AND id_componente IS NOT NULL"), 
            name='check_stock_exclusive_relation'
        ),
        CheckConstraint("cantidad_actual >= 0", name='check_cantidad_actual_positiva'),
        CheckConstraint("cantidad_minima >= 0", name='check_cantidad_minima_positiva'),
        CheckConstraint("cantidad_maxima IS NULL OR cantidad_maxima >= 0", name='check_cantidad_maxima_positiva'),
        CheckConstraint("cantidad_maxima IS NULL OR cantidad_maxima >= cantidad_minima", name='check_stock_range'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    cantidad_actual = Column(Numeric(10, 2), nullable=False, default=0)
    cantidad_minima = Column(Numeric(10, 2), default=0)
    cantidad_maxima = Column(Numeric(10, 2))
    ubicacion_almacen = Column(String(255))  # Pasillo, estantería, etc.
    
    # Foreign Keys (solo uno debe estar presente)
    id_producto_simple = Column(Integer, ForeignKey("producto_simple.id"), unique=True)
    id_componente = Column(Integer, ForeignKey("componente.id"), unique=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    producto_simple = relationship("ProductoSimple", back_populates="stock")
    componente = relationship("Componente", back_populates="stock")
    
    @property
    def elemento(self):
        """Retorna el elemento (producto simple o componente) asociado al stock"""
        return self.producto_simple or self.componente
    
    @property
    def nombre_elemento(self):
        """Retorna el nombre del elemento en stock"""
        if self.producto_simple:
            return self.producto_simple.producto.articulo.nombre
        elif self.componente:
            return self.componente.nombre
        return "Sin elemento"
    
    @property
    def necesita_reposicion(self):
        """Indica si el stock está por debajo del mínimo"""
        return self.cantidad_actual <= self.cantidad_minima
    
    def __repr__(self):
        return f"<Stock(id={self.id}, cantidad={self.cantidad_actual}, elemento='{self.nombre_elemento}')>"
