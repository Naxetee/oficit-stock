from typing import Optional
from sqlalchemy import Integer, String, Text, Boolean, CheckConstraint, ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base

class Articulo(Base):
    __tablename__ = 'Articulo'
    __table_args__ = (
        CheckConstraint("tipo IS NULL OR (tipo::text = ANY (ARRAY['simple', 'compuesto', 'pack']))", name='Articulo_tipo_check'),
        ForeignKeyConstraint(['id_familia'], ['Familia.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Articulo_id_familia_fkey'),
        PrimaryKeyConstraint('id', name='Articulo_pkey'),
        UniqueConstraint('codigo_tienda', name='Articulo_codigo_tienda_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[Optional[str]] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    codigo_tienda: Mapped[Optional[str]] = mapped_column(String(31))
    id_familia: Mapped[Optional[int]] = mapped_column(Integer)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean)

    Familia_: Mapped[Optional['Familia']] = relationship('Familia', back_populates='Articulo')

    def __repr__(self):
        return f"({self.id}) {self.nombre}"
