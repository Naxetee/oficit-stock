from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Proveedor(Base):
    """
    🏢 Proveedor - Almacena la información de los proveedores
    
    Esta clase gestiona los datos de los proveedores que suministran
    productos simples y componentes a la empresa.
    
    Attributes:
        id (int): Identificador único del proveedor
        nombre (str): Nombre o razón social del proveedor
        nif_cif (str): Número de identificación fiscal (único)
        direccion (str): Dirección completa del proveedor
        telefono (str): Número de teléfono de contacto
        email (str): Correo electrónico de contacto
        activo (bool): Indica si el proveedor está activo
        created_at (datetime): Fecha y hora de creación
        updated_at (datetime): Fecha y hora de última actualización
        
    Relationships:
        productos_simples (List[ProductoSimple]): Productos suministrados
        componentes (List[Componente]): Componentes suministrados
    """
    __tablename__ = "proveedor"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    nif_cif = Column(String(20), unique=True)
    direccion = Column(Text)
    telefono = Column(String(20))
    email = Column(String(100))
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    productos_simples = relationship("ProductoSimple", back_populates="proveedor")
    componentes = relationship("Componente", back_populates="proveedor")
    
    def __repr__(self):
        return f"<Proveedor(id={self.id}, nombre='{self.nombre}')>"
