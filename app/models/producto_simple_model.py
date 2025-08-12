from typing import List, Optional
from sqlalchemy import Integer, String, Text, Boolean, CheckConstraint, ForeignKeyConstraint, PrimaryKeyConstraint, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base_model import Base
from .producto_model import Producto
import datetime


class ProductoSimple(Producto):
    __tablename__ = 'Producto_Simple'
    __table_args__ = (
        CheckConstraint("tipo IS NULL OR (tipo::text = ANY (ARRAY['simple', 'compuesto', 'pack']))", name='Articulo_tipo_check'),
        ForeignKeyConstraint(['id_color'], ['Color.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Producto_Simple_id_color_fkey'),
        ForeignKeyConstraint(['id_proveedor'], ['Proveedor.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Producto_Simple_id_proveedor_fkey'),
        PrimaryKeyConstraint('id', name='Producto_Simple_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, ForeignKey('Producto.id'), primary_key=True)
    id_proveedor: Mapped[Optional[int]] = mapped_column(Integer)
    id_color: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    Color_: Mapped[Optional['Color']] = relationship('Color', back_populates='Producto_Simple')
    Proveedor_: Mapped[Optional['Proveedor']] = relationship('Proveedor', back_populates='Producto_Simple')
    Stock: Mapped[List['Stock']] = relationship('Stock', back_populates='Producto_Simple')

    __mapper_args__ = {
        "polymorphic_identity": "simple",
        "concrete": False,
    }

    def __repr__(self):
        return f"({self.id}) {self.nombre}"
        return f"({self.id}) {self.nombre}"
