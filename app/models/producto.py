from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Producto(Base):
    """
    📦 Producto - Representa un producto final que se vende
    
    Un producto puede ser simple (vendido tal cual) o compuesto (ensamblado
    a partir de varios componentes). Está vinculado a un artículo para
    heredar información general.
    
    Attributes:
        id (int): Identificador único del producto
        tipo_producto (str): Tipo ('simple' o 'compuesto')
        id_articulo (int): Referencia al artículo asociado (única)
        created_at (datetime): Fecha y hora de creación
        updated_at (datetime): Fecha y hora de última actualización
        
    Relationships:
        articulo (Articulo): Artículo asociado con información general
        producto_simple (ProductoSimple): Detalle si es producto simple
        producto_compuesto (ProductoCompuesto): Detalle si es compuesto
        pack_productos (List[PackProducto]): Packs que incluyen este producto
    """
    __tablename__ = "producto"
    
    # Restricción a nivel de base de datos para tipo_producto
    __table_args__ = (
        CheckConstraint("tipo_producto IN ('simple', 'compuesto')", name='check_tipo_producto'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_producto = Column(String(20), nullable=False)  # 'simple' o 'compuesto'
    
    # Foreign Keys
    id_articulo = Column(Integer, ForeignKey("articulo.id"), nullable=False, unique=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    articulo = relationship("Articulo", back_populates="producto")
    
    # Relación polimórfica con ProductoSimple o ProductoCompuesto
    producto_simple = relationship("ProductoSimple", back_populates="producto", uselist=False)
    producto_compuesto = relationship("ProductoCompuesto", back_populates="producto", uselist=False)
    
    # Relación con Pack (many-to-many a través de tabla intermedia)
    pack_productos = relationship("PackProducto", back_populates="producto")
    
    @property
    def detalle(self):
        """Retorna el detalle específico del producto (simple o compuesto)"""
        if self.tipo_producto == 'simple':
            return self.producto_simple
        elif self.tipo_producto == 'compuesto':
            return self.producto_compuesto
        return None
    
    def __repr__(self):
        return f"<Producto(id={self.id}, tipo='{self.tipo_producto}')>"
