from typing import Optional
from sqlalchemy import CheckConstraint, Integer, String, ForeignKeyConstraint, PrimaryKeyConstraint, DateTime, text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base
import datetime


class Stock(Base):
    __tablename__ = 'Stock'
    __table_args__ = (
        CheckConstraint("tipo::text = 'componente'::text AND id_componente IS NOT NULL AND id_producto_simple IS NULL OR tipo::text = 'producto_simple'::text AND id_producto_simple IS NOT NULL AND id_componente IS NULL", name='Stock_check'),
        CheckConstraint("tipo::text = ANY (ARRAY['producto_simple'::character varying, 'componente'::character varying]::text[])", name='Stock_tipo_check'),
        ForeignKeyConstraint(['id_componente'], ['Componente.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Stock_id_componente_fkey'),
        ForeignKeyConstraint(['id_producto_simple'], ['Producto_Simple.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Stock_id_producto_simple_fkey'),
        PrimaryKeyConstraint('id', name='Stock_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    cantidad: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    cantidad_minima: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    tipo: Mapped[str] = mapped_column(String(31))
    ubicacion: Mapped[Optional[str]] = mapped_column(String(255))
    id_componente: Mapped[Optional[int]] = mapped_column(Integer)
    id_producto_simple: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    Componente_: Mapped[Optional['Componente']] = relationship('Componente', back_populates='Stock')
    Producto_Simple: Mapped[Optional['ProductoSimple']] = relationship('ProductoSimple', back_populates='Stock')

    def __repr__(self):
        return f"({self.id}) {getattr(self, 'id_componente', '') or getattr(self, 'id_producto_simple', '')} - Cantidad: {self.cantidad}/{self.cantidad_minima}"
