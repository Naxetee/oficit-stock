from typing import Optional, List
from sqlalchemy import Integer, String, Boolean, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base
from models import *


class Proveedor(Base):
    __tablename__ = 'Proveedor'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='Proveedor_pkey'),
        UniqueConstraint('nombre', name='Proveedor_nombre_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(127))
    telefono: Mapped[Optional[str]] = mapped_column(String(31))
    email: Mapped[Optional[str]] = mapped_column(String(127))
    direccion: Mapped[Optional[str]] = mapped_column(String(255))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean)

    Componente: Mapped[List['Componente']] = relationship('Componente', back_populates='Proveedor_')
    Producto_Simple: Mapped[List['ProductoSimple']] = relationship('ProductoSimple', back_populates='Proveedor_')
