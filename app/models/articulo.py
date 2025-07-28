from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Articulo(Base):
    """
    📄 Artículo - Entidad central que representa cualquier elemento gestionado en el inventario
    Args:
        id (int): Identificador único del artículo.
        nombre (str): Nombre del artículo.
        descripcion (str): Descripción detallada del artículo.
        sku (str): Código único del artículo.
        activo (bool): Indica si el artículo está activo.
        id_familia (int): Identificador de la familia a la que pertenece el artículo
        id_precio_venta (int): Identificador del precio de venta asociado al artículo.
    Relaciones:
        familia (Familia): Relación con la familia del artículo.
        precio_venta (PrecioVenta): Relación con el precio de venta del artículo.
        producto (Producto): Relación polimórfica con un producto simple.
        pack (Pack): Relación polimórfica con un pack de productos.
    """
    __tablename__ = "articulo"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    sku = Column(String(50), unique=True)
    activo = Column(Boolean, default=True)
    
    # Foreign Keys
    id_familia = Column(Integer, ForeignKey("familia.id"), nullable=False)
    id_precio_venta = Column(Integer, ForeignKey("precio_venta.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    familia = relationship("Familia", back_populates="articulos")
    precio_venta = relationship("PrecioVenta", back_populates="articulos")
    
    # Relación polimórfica con Producto o Pack
    producto = relationship("Producto", back_populates="articulo", uselist=False)
    pack = relationship("Pack", back_populates="articulo", uselist=False)
    
    @property
    def tipo_elemento(self):
        """Retorna si es un producto o un pack"""
        if self.producto:
            return "producto"
        elif self.pack:
            return "pack"
        return None
    
    def __repr__(self):
        return f"<Articulo(id={self.id}, nombre='{self.nombre}', sku='{self.sku}')>"