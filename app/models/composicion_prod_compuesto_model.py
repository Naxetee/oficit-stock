from sqlalchemy import Integer, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base


class ComposicionProdCompuesto(Base):
    __tablename__ = 'Composicion_Prod_Compuesto'
    __table_args__ = (
        ForeignKeyConstraint(['id_componente'], ['Componente.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Composicion_Prod.Compuesto_id_componente_fkey'),
        ForeignKeyConstraint(['id_producto_compuesto'], ['Producto_Compuesto.id'], ondelete='CASCADE', onupdate='CASCADE', name='Composicion_Prod.Compuesto_id_producto_compuesto_fkey'),
        PrimaryKeyConstraint('id_producto_compuesto', 'id_componente', name='Composicion_Prod.Compuesto_pkey')
    )

    id_producto_compuesto: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_componente: Mapped[int] = mapped_column(Integer, primary_key=True)
    cantidad: Mapped[int] = mapped_column(Integer)

    Componente_: Mapped['Componente'] = relationship('Componente', back_populates='Composicion_Prod_Compuesto')
    Producto_Compuesto: Mapped['ProductoCompuesto'] = relationship('ProductoCompuesto', back_populates='Composicion_Prod_Compuesto')
