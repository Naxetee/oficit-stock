from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Familia(Base):
    """
    🏷️ Familia - Agrupa y clasifica los artículos en categorías lógicas
    
    Esta clase representa las categorías principales para organizar los artículos
    del inventario (ej: mesas, sillas, accesorios, etc.)
    
    Attributes:
        id (int): Identificador único de la familia
        nombre (str): Nombre de la familia (único en el sistema)
        descripcion (str): Descripción detallada de la familia
        created_at (datetime): Fecha y hora de creación
        updated_at (datetime): Fecha y hora de última actualización
        
    Relationships:
        articulos (List[Articulo]): Lista de artículos que pertenecen a esta familia
    """
    __tablename__ = "familia"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    articulos = relationship("Articulo", back_populates="familia")
    
    def __repr__(self):
        return f"<Familia(id={self.id}, nombre='{self.nombre}')>"
