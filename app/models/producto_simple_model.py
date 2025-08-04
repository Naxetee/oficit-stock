from typing import Optional
from sqlalchemy import Integer, String, Text, Boolean, CheckConstraint, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base

class ProductoSimple(Base):
    __tablename__ = 'Producto_Simple'
    __table_args__ = (
        CheckConstraint("tipo IS NULL OR (tipo::text = ANY (ARRAY['simple', 'compuesto', 'pack']))", name='Articulo_tipo_check'),
        ForeignKeyConstraint(['id_color'], ['Color.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Producto_Simple_id_color_fkey'),
        ForeignKeyConstraint(['id_proveedor'], ['Proveedor.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Producto_Simple_id_proveedor_fkey'),
        PrimaryKeyConstraint('id', name='Producto_Simple_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[Optional[str]] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    codigo_tienda: Mapped[Optional[str]] = mapped_column(String(31))
    id_familia: Mapped[Optional[int]] = mapped_column(Integer)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean)
    id_proveedor: Mapped[Optional[int]] = mapped_column(Integer)
    id_color: Mapped[Optional[int]] = mapped_column(Integer)

    Color_: Mapped[Optional['Color']] = relationship('Color', back_populates='Producto_Simple')
    Proveedor_: Mapped[Optional['Proveedor']] = relationship('Proveedor', back_populates='Producto_Simple')
