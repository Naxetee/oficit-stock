from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class ProductoSimple(Base):
    """
    🪑 Producto_Simple - Producto que se vende tal cual, sin componentes internos
    
    Representa productos que se compran directamente a proveedores y se venden
    sin necesidad de ensamblaje o fabricación adicional.
    
    Attributes:
        id (int): Identificador único del producto simple
        especificaciones (str): Detalles técnicos del producto
        id_producto (int): Referencia al producto base (única)
        id_proveedor (int): Referencia al proveedor que lo suministra
        id_color (int): Referencia al color del producto (opcional)
        id_familia (int, opcional): Referencia a la familia del producto
        created_at (datetime): Fecha y hora de creación
        updated_at (datetime): Fecha y hora de última actualización
        
    Relationships:
        producto (Producto): Producto base asociado
        proveedor (Proveedor): Proveedor que suministra el producto
        color (Color): Color del producto (si aplica)
        stock (Stock): Información de stock del producto
    """
    __tablename__ = "producto_simple"
    
    id = Column(Integer, primary_key=True, index=True)
    especificaciones = Column(Text)  # Detalles específicos del producto
    
    # Foreign Keys
    id_producto = Column(Integer, ForeignKey("producto.id"), nullable=False, unique=True)
    id_proveedor = Column(Integer, ForeignKey("proveedor.id"))
    id_color = Column(Integer, ForeignKey("color.id"))
    id_familia = Column(Integer, ForeignKey("familia.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    producto = relationship("Producto", back_populates="producto_simple")
    proveedor = relationship("Proveedor", back_populates="productos_simples")
    color = relationship("Color", back_populates="productos_simples")
    stock = relationship("Stock", back_populates="producto_simple", uselist=False)
    
    def __repr__(self):
        return f"<ProductoSimple(id={self.id})>"
