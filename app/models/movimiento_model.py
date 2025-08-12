import datetime
from typing import Optional
from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Identity, Integer, PrimaryKeyConstraint, String, Text, func
from app.models.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship



class Movimiento(Base):
    __tablename__ = 'Movimiento'
    __table_args__ = (
        CheckConstraint("tipo::text = ANY (ARRAY['entrada'::character varying, 'salida'::character varying]::text[])", name='Movimiento_tipo_check'),
        ForeignKeyConstraint(
            ['id_producto_simple'], ['Producto_Simple.id'],
            ondelete='RESTRICT', onupdate='CASCADE',
            name='Movimiento_id_producto_simple_fkey'
        ),
        ForeignKeyConstraint(
            ['id_componente'], ['Componente.id'],
            ondelete='RESTRICT', onupdate='CASCADE',
            name='Movimiento_id_componente_fkey'
        ),
        PrimaryKeyConstraint('id', name='Movimiento_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    tipo: Mapped[str] = mapped_column(String(31))
    cantidad: Mapped[int] = mapped_column(Integer)
    id_producto_simple: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    id_componente: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        if self.id_producto_simple is not None:
            return f"({self.id}) {self.tipo} - Cantidad: {self.cantidad} - Producto Simple ID: {self.id_producto_simple}"
        else:
            return f"({self.id}) {self.tipo} - Cantidad: {self.cantidad} - Componente ID: {self.id_componente}"