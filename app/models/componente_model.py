from typing import Optional, List
from sqlalchemy import Integer, String, Text, ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base
from models import *

class Componente(Base):
    __tablename__ = 'Componente'
    __table_args__ = (
        ForeignKeyConstraint(['id_color'], ['Color.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Componente_id_color_fkey'),
        ForeignKeyConstraint(['id_proveedor'], ['Proveedor.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Componente_id_proveedor_fkey'),
        PrimaryKeyConstraint('id', name='Componente_pkey'),
        UniqueConstraint('nombre', name='Componente_nombre_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    id_proveedor: Mapped[Optional[int]] = mapped_column(Integer)
    id_color: Mapped[Optional[int]] = mapped_column(Integer)

    Color_: Mapped[Optional['Color']] = relationship('Color', back_populates='Componente')
    Proveedor_: Mapped[Optional['Proveedor']] = relationship('Proveedor', back_populates='Componente')
    Composicion_Prod_Compuesto: Mapped[List['ComposicionProdCompuesto']] = relationship('ComposicionProdCompuesto', back_populates='Componente_')
