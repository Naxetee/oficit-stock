from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Color(Base):
    """
    🎨 Color - Define los colores disponibles para productos simples y componentes
    
    Esta clase gestiona los colores que pueden tener los productos simples y componentes,
    permitiendo variantes de color para el mismo elemento base.
    
    Attributes:
        id (int): Identificador único del color
        nombre (str): Nombre del color (único en el sistema)
        codigo_hex (str, opcional): Código hexadecimal del color 
        url_imagen (str): URL de imagen representativa del color
        activo (bool): Indica si el color está disponible
        descripcion (str, opcional): Descripción del color 
        id_familia (int, opcional): Referencia a familia de colores 
        created_at (datetime): Fecha y hora de creación
        updated_at (datetime): Fecha y hora de última actualización
        
    Relationships:
        productos_simples (List[ProductoSimple]): Productos que usan este color
        componentes (List[Componente]): Componentes que tienen este color
    """
    __tablename__ = "color"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    codigo_hex = Column(String(7))  # Código hexadecimal del color (ej: #FF0000)
    url_imagen = Column(String(2000))  # URL de la imagen del color
    activo = Column(Boolean, default=True)
    id_familia = Column(Integer, ForeignKey("familia.id"))  # Relación con familia de colores
    descripcion = Column(Text, nullable=True)  # Descripción del color
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    productos_simples = relationship("ProductoSimple", back_populates="color")
    componentes = relationship("Componente", back_populates="color")
    
    def __repr__(self):
        return f"<Color(id={self.id}, nombre='{self.nombre}')>"
