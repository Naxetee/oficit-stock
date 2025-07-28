from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class PackProducto(Base):
    """
    🔗 PackProducto - Tabla intermedia para relación many-to-many entre Pack y Producto
    
    Esta tabla define qué productos están incluidos en cada pack y en qué cantidades,
    permitiendo crear ofertas especiales con múltiples productos.
    
    Attributes:
        id (int): Identificador único de la relación
        cantidad_incluida (Decimal): Cantidad del producto incluida en el pack
        id_pack (int): Referencia al pack que contiene el producto
        id_producto (int): Referencia al producto incluido
        created_at (datetime): Fecha de creación de la relación
        updated_at (datetime): Fecha de última actualización
        
    Relationships:
        pack (Pack): Pack que contiene el producto
        producto (Producto): Producto incluido en el pack
    """
    __tablename__ = "pack_producto"
    
    # Restricciones de integridad
    __table_args__ = (
        CheckConstraint("cantidad_incluida > 0", name='check_cantidad_incluida_positiva'),
        UniqueConstraint('id_pack', 'id_producto', name='uk_pack_producto'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    cantidad_incluida = Column(Numeric(10, 2), nullable=False, default=1)
    
    # Foreign Keys
    id_pack = Column(Integer, ForeignKey("pack.id"), nullable=False)
    id_producto = Column(Integer, ForeignKey("producto.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    pack = relationship("Pack", back_populates="pack_productos")
    producto = relationship("Producto", back_populates="pack_productos")
    
    def __repr__(self):
        return f"<PackProducto(pack_id={self.id_pack}, producto_id={self.id_producto}, cantidad={self.cantidad_incluida})>"
