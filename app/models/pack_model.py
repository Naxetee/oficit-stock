from typing import Optional
from sqlalchemy import Integer, String, Text, Boolean, CheckConstraint, PrimaryKeyConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base_model import Base
import datetime


class Pack(Base):
    __tablename__ = 'Pack'
    __table_args__ = (
        CheckConstraint("tipo IS NULL OR (tipo::text = ANY (ARRAY['simple', 'compuesto', 'pack']))", name='Articulo_tipo_check'),
        PrimaryKeyConstraint('id', name='Pack_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[Optional[str]] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    codigo_tienda: Mapped[Optional[str]] = mapped_column(String(31))
    id_familia: Mapped[Optional[int]] = mapped_column(Integer)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    Composicion_Pack: Mapped['ComposicionPack'] = relationship('ComposicionPack', uselist=False, back_populates='Pack_')
    Composicion_Pack: Mapped['ComposicionPack'] = relationship('ComposicionPack', uselist=False, back_populates='Pack_')
