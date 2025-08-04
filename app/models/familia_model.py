from typing import List, Optional
from sqlalchemy import Integer, String, Text, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base

class Familia(Base):
    __tablename__ = 'Familia'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='Familia_pkey'),
        UniqueConstraint('nombre', name='Familia_nombre_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(127))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    Articulo: Mapped[List['Articulo']] = relationship('Articulo', back_populates='Familia_')
    Color: Mapped[List['Color']] = relationship('Color', back_populates='Familia_')
