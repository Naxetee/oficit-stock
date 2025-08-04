from typing import Optional, List
from sqlalchemy import Integer, String, Text, ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base_model import Base
import datetime

class Color(Base):
    __tablename__ = 'Color'
    __table_args__ = (
        ForeignKeyConstraint(['id_familia'], ['Familia.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Color_id_familia_fkey'),
        PrimaryKeyConstraint('id', name='Color_pkey'),
        UniqueConstraint('nombre', name='Color_nombre_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(31))
    hex: Mapped[Optional[str]] = mapped_column(String(7))
    url_imagen: Mapped[Optional[str]] = mapped_column(String(511))
    id_familia: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    Familia_: Mapped[Optional['Familia']] = relationship('Familia', back_populates='Color')
    Componente: Mapped[List['Componente']] = relationship('Componente', back_populates='Color_')
    Producto_Simple: Mapped[List['ProductoSimple']] = relationship('ProductoSimple', back_populates='Color_')
    Producto_Simple: Mapped[List['ProductoSimple']] = relationship('ProductoSimple', back_populates='Color_')
