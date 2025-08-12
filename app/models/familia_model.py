from typing import List, Optional
from sqlalchemy import Integer, String, Text, PrimaryKeyConstraint, UniqueConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base_model import Base
import datetime


class Familia(Base):
    __tablename__ = 'Familia'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='Familia_pkey'),
        UniqueConstraint('nombre', name='Familia_nombre_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(127))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    Articulo: Mapped[List['Articulo']] = relationship('Articulo', back_populates='Familia_')
    Color: Mapped[List['Color']] = relationship('Color', back_populates='Familia_')

    def __repr__(self):
        return f"({self.id}) {self.nombre}"
