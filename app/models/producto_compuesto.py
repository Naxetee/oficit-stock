from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class ProductoCompuesto(Base):
    """
    🛠️ Producto_Compuesto - Producto que se ensambla a partir de varios componentes
    
    Representa productos que se fabrican internamente combinando múltiples
    componentes según especificaciones de ensamblaje.
    
    Attributes:
        id (int): Identificador único del producto compuesto
        id_producto (int): Referencia al producto base (única)
        id_familia (int, opcional): Referencia a la familia del producto
        instrucciones_ensamblaje (str): Instrucciones para fabricar el producto
        tiempo_fabricacion (int): Tiempo estimado en minutos
        created_at (datetime): Fecha y hora de creación
        updated_at (datetime): Fecha y hora de última actualización
        
    Relationships:
        producto (Producto): Producto base asociado
        componente_productos (List[ComponenteProducto]): Componentes necesarios
        
    Properties:
        componentes: Lista de componentes requeridos para este producto
    """
    __tablename__ = "producto_compuesto"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    id_producto = Column(Integer, ForeignKey("producto.id"), nullable=False, unique=True)
    id_familia = Column(Integer, ForeignKey("familia.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    producto = relationship("Producto", back_populates="producto_compuesto")
    
    # Relación con componentes (many-to-many a través de tabla intermedia)
    componente_productos = relationship("ComponenteProducto", back_populates="producto_compuesto")
    
    @property
    def componentes(self):
        """Retorna la lista de componentes con sus cantidades"""
        return [cp.componente for cp in self.componente_productos]
    
    def __repr__(self):
        return f"<ProductoCompuesto(id={self.id})>"
