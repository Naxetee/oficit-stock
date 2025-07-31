from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Pack(Base):
    """
    🎁 Pack - Conjunto de productos que se venden juntos como una oferta especial
    
    Attributes:
        id (int): Identificador único del pack
        nombre (str): Nombre comercial del pack
        descripcion (str): Descripción detallada del pack
        id_articulo (int): Referencia al artículo asociado (única)
        created_at (datetime): Fecha y hora de creación
        updated_at (datetime): Fecha y hora de última actualización
        
    Relationships:
        articulo (Articulo): Artículo asociado con información general
        pack_productos (List[PackProducto]): Productos incluidos en el pack
        
    Properties:
        productos: Lista de productos que componen el pack
    """
    __tablename__ = "pack"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    
    # Foreign Keys
    id_articulo = Column(Integer, ForeignKey("Articulo.id"), nullable=False, unique=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    articulo = relationship("Articulo", back_populates="pack")
    
    # Relación con productos (many-to-many a través de tabla intermedia)
    pack_productos = relationship("PackProducto", back_populates="pack")
    
    @property
    def productos(self):
        """Retorna la lista de productos con sus cantidades"""
        return [pp.producto for pp in self.pack_productos]
    
    def __repr__(self):
        return f"<Pack(id={self.id}, nombre='{self.nombre}')>"
