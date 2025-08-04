from typing import Optional, List
from sqlalchemy import Integer, String, Text, Boolean, CheckConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base


class Producto(Base):
    __tablename__ = 'Producto'
    __table_args__ = (
        CheckConstraint("tipo IS NULL OR (tipo::text = ANY (ARRAY['simple', 'compuesto', 'pack']))", name='Articulo_tipo_check'),
        PrimaryKeyConstraint('id', name='Producto_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[Optional[str]] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    codigo_tienda: Mapped[Optional[str]] = mapped_column(String(31))
    id_familia: Mapped[Optional[int]] = mapped_column(Integer)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean)

    Composicion_Pack: Mapped[List['ComposicionPack']] = relationship('ComposicionPack', back_populates='Producto_')
