from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class ComponenteProducto(Base):
    """
    🔗 ComponenteProducto - Tabla intermedia para relación many-to-many entre Componente y ProductoCompuesto
    
    Esta tabla define qué componentes se necesitan para fabricar cada producto compuesto
    y en qué cantidades específicas.
    
    Attributes:
        id (int): Identificador único de la relación
        cantidad_necesaria (Decimal): Cantidad del componente necesaria
        id_componente (int): Referencia al componente requerido
        id_producto_compuesto (int): Referencia al producto que lo necesita
        created_at (datetime): Fecha de creación de la relación
        updated_at (datetime): Fecha de última actualización
        
    Relationships:
        componente (Componente): Componente requerido
        producto_compuesto (ProductoCompuesto): Producto que necesita el componente
    """
    __tablename__ = "componente_producto"
    
    # Restricciones de integridad
    __table_args__ = (
        CheckConstraint("cantidad_necesaria > 0", name='check_cantidad_necesaria_positiva'),
        UniqueConstraint('id_componente', 'id_producto_compuesto', name='uk_componente_producto'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    cantidad_necesaria = Column(Numeric(10, 2), nullable=False)
    
    # Foreign Keys
    id_componente = Column(Integer, ForeignKey("componente.id"), nullable=False)
    id_producto_compuesto = Column(Integer, ForeignKey("producto_compuesto.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    componente = relationship("Componente", back_populates="componente_productos")
    producto_compuesto = relationship("ProductoCompuesto", back_populates="componente_productos")
    
    def __repr__(self):
        return f"<ComponenteProducto(componente_id={self.id_componente}, producto_id={self.id_producto_compuesto}, cantidad={self.cantidad_necesaria})>"
