from sqlalchemy import Column, DateTime, Integer, String, Text, DECIMAL, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db import Base

class Componente(Base):
    """
    🔩 Componente - Partes individuales que se compran a proveedores para fabricar productos compuestos
    
    Representa las piezas básicas que se adquieren de proveedores y se utilizan
    como materia prima para ensamblar productos compuestos.
    
    Attributes:
        id (int): Identificador único del componente
        nombre (str): Nombre descriptivo del componente
        descripcion (str): Descripción detallada del componente
        codigo (str): Código único del componente (SKU interno)
        especificaciones (str): Especificaciones técnicas
        unidad_medida (str): Unidad de medida (unidad, metro, kg, etc.)
        id_proveedor (int): Referencia al proveedor que lo suministra
        id_color (int, opcional): Referencia al color del componente
        id_familia (int, opcional): Referencia a la familia del componente
        created_at (datetime): Fecha y hora de creación
        updated_at (datetime): Fecha y hora de última actualización
        
    Relationships:
        proveedor (Proveedor): Proveedor que suministra el componente
        color (Color): Color del componente (si aplica)
        stock (Stock): Información de stock del componente
        componente_productos (List[ComponenteProducto]): Productos que usan este componente
    """
    __tablename__ = "componente"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    codigo = Column(String(50), unique=True)
    especificaciones = Column(Text)
    
    # Foreign Keys
    id_proveedor = Column(Integer, ForeignKey("proveedor.id"))
    id_color = Column(Integer, ForeignKey("color.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    proveedor = relationship("Proveedor", back_populates="componentes")
   
    color = relationship("Color", back_populates="componentes")
    stock = relationship("Stock", back_populates="componente", uselist=False)
    productos_que_lo_usan = relationship("ComponenteProducto", back_populates="componente")
    
    def __repr__(self):
        return f"<Componente(id={self.id}, nombre='{self.nombre}', codigo='{self.codigo}')>"
