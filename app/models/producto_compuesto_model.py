from typing import Optional, List
from sqlalchemy import Integer, String, Text, Boolean, CheckConstraint, PrimaryKeyConstraint, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.composicion_prod_compuesto_model import ComposicionProdCompuesto
from .base_model import Base
from .producto_model import Producto
import datetime


class ProductoCompuesto(Producto):
    __tablename__ = 'Producto_Compuesto'
    __table_args__ = (
        CheckConstraint("tipo IS NULL OR (tipo::text = ANY (ARRAY['simple', 'compuesto', 'pack']))", name='Articulo_tipo_check'),
        PrimaryKeyConstraint('id', name='Producto_Compuesto_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, ForeignKey('Producto.id'), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    Composicion_Prod_Compuesto: Mapped[List['ComposicionProdCompuesto']] = relationship('ComposicionProdCompuesto', back_populates='Producto_Compuesto')

    __mapper_args__ = {
        "polymorphic_identity": "compuesto",
        "concrete": False,
    }

    def __repr__(self):
        return f"({self.id}) {self.nombre}"