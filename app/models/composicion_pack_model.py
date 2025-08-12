from sqlalchemy import Integer, PrimaryKeyConstraint, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base

class ComposicionPack(Base):
    __tablename__ = 'Composicion_Pack'
    __table_args__ = (
        ForeignKeyConstraint(['id_pack'], ['Pack.id'], ondelete='CASCADE', onupdate='CASCADE', name='Composicion_Pack_id_pack_fkey'),
        ForeignKeyConstraint(['id_producto'], ['Producto.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Composicion_Pack_id_producto_fkey'),
        PrimaryKeyConstraint('id_pack', 'id_producto', name='Composicion_Pack_pkey'),
        UniqueConstraint('id_pack', name='Composicion_Pack_id_pack_key')
    )

    id_pack: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_producto: Mapped[int] = mapped_column(Integer, primary_key=True)
    cantidad: Mapped[int] = mapped_column(Integer)

    Pack_: Mapped['Pack'] = relationship('Pack', back_populates='Composicion_Pack')
    Producto_: Mapped['Producto'] = relationship('Producto', back_populates='Composicion_Pack')

    def __repr__(self):
        return f"({self.id_pack}) {self.id_producto} - Cantidad: {self.cantidad}"