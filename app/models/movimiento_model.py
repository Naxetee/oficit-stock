from datetime import datetime
from typing import Optional
from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Identity, Integer, PrimaryKeyConstraint, String, Text, func
from app.models.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship



class Movimiento(Base):
    __tablename__ = 'Movimiento'
    __table_args__ = (
        CheckConstraint("tipo::text = ANY (ARRAY['entrada'::character varying, 'salida'::character varying]::text[])", name='Movimiento_tipo_check'),
        ForeignKeyConstraint(['id_stock'], ['Stock.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Movimiento_id_stock_fkey'),
        PrimaryKeyConstraint('id', name='Movimiento_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    tipo: Mapped[str] = mapped_column(String(31))
    cantidad: Mapped[int] = mapped_column(Integer)
    id_stock: Mapped[int] = mapped_column(Integer)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    Stock_: Mapped['Stock'] = relationship('Stock', back_populates='Movimiento')