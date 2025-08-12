from typing import Optional, List
from sqlalchemy import Integer, String, Boolean, PrimaryKeyConstraint, UniqueConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base_model import Base
import datetime


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
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    Componente: Mapped[List['Componente']] = relationship('Componente', back_populates='Proveedor_')
    Producto_Simple: Mapped[List['ProductoSimple']] = relationship('ProductoSimple', back_populates='Proveedor_')

    def __repr__(self):
        return f"({self.id}) {self.nombre}"
