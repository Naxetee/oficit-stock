from typing import List, Optional

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKeyConstraint, Identity, Integer, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Familia(Base):
    __tablename__ = 'Familia'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='Familia_pkey'),
        UniqueConstraint('nombre', name='Familia_nombre_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(127))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    Articulo: Mapped[List['Articulo']] = relationship('Articulo', back_populates='Familia_')
    Color: Mapped[List['Color']] = relationship('Color', back_populates='Familia_')


class Pack(Base):
    __tablename__ = 'Pack'
    __table_args__ = (
        CheckConstraint("tipo IS NULL OR (tipo::text = ANY (ARRAY['simple'::character varying, 'compuesto'::character varying, 'pack'::character varying]::text[]))", name='Articulo_tipo_check'),
        PrimaryKeyConstraint('id', name='Pack_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    tipo: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[Optional[str]] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    codigo_tienda: Mapped[Optional[str]] = mapped_column(String(31))
    id_familia: Mapped[Optional[int]] = mapped_column(Integer)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    Composicion_Pack: Mapped[List['ComposicionPack']] = relationship('ComposicionPack', back_populates='Pack_')


class Producto(Base):
    __tablename__ = 'Producto'
    __table_args__ = (
        CheckConstraint("tipo IS NULL OR (tipo::text = ANY (ARRAY['simple'::character varying, 'compuesto'::character varying, 'pack'::character varying]::text[]))", name='Articulo_tipo_check'),
        PrimaryKeyConstraint('id', name='Producto_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[Optional[str]] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    codigo_tienda: Mapped[Optional[str]] = mapped_column(String(31))
    id_familia: Mapped[Optional[int]] = mapped_column(Integer)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    Composicion_Pack: Mapped[List['ComposicionPack']] = relationship('ComposicionPack', back_populates='Producto_')


class ProductoCompuesto(Base):
    __tablename__ = 'Producto_Compuesto'
    __table_args__ = (
        CheckConstraint("tipo IS NULL OR (tipo::text = ANY (ARRAY['simple'::character varying, 'compuesto'::character varying, 'pack'::character varying]::text[]))", name='Articulo_tipo_check'),
        PrimaryKeyConstraint('id', name='Producto_Compuesto_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[Optional[str]] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    codigo_tienda: Mapped[Optional[str]] = mapped_column(String(31))
    id_familia: Mapped[Optional[int]] = mapped_column(Integer)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    Composicion_Prod_Compuesto: Mapped[List['ComposicionProdCompuesto']] = relationship('ComposicionProdCompuesto', back_populates='Producto_Compuesto')


class Proveedor(Base):
    __tablename__ = 'Proveedor'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='Proveedor_pkey'),
        UniqueConstraint('nombre', name='Proveedor_nombre_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(127))
    telefono: Mapped[Optional[str]] = mapped_column(String(31))
    email: Mapped[Optional[str]] = mapped_column(String(127))
    direccion: Mapped[Optional[str]] = mapped_column(String(255))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    Componente: Mapped[List['Componente']] = relationship('Componente', back_populates='Proveedor_')
    Producto_Simple: Mapped[List['ProductoSimple']] = relationship('ProductoSimple', back_populates='Proveedor_')


class Articulo(Base):
    __tablename__ = 'Articulo'
    __table_args__ = (
        CheckConstraint("tipo IS NULL OR (tipo::text = ANY (ARRAY['simple'::character varying, 'compuesto'::character varying, 'pack'::character varying]::text[]))", name='Articulo_tipo_check'),
        ForeignKeyConstraint(['id_familia'], ['Familia.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Articulo_id_familia_fkey'),
        PrimaryKeyConstraint('id', name='Articulo_pkey'),
        UniqueConstraint('codigo_tienda', name='Articulo_codigo_tienda_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    tipo: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[Optional[str]] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    codigo_tienda: Mapped[Optional[str]] = mapped_column(String(31))
    id_familia: Mapped[Optional[int]] = mapped_column(Integer)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    Familia_: Mapped[Optional['Familia']] = relationship('Familia', back_populates='Articulo')


class Color(Base):
    __tablename__ = 'Color'
    __table_args__ = (
        ForeignKeyConstraint(['id_familia'], ['Familia.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Color_id_familia_fkey'),
        PrimaryKeyConstraint('id', name='Color_pkey'),
        UniqueConstraint('nombre', name='Color_nombre_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(31))
    hex: Mapped[Optional[str]] = mapped_column(String(7))
    url_imagen: Mapped[Optional[str]] = mapped_column(String(511))
    id_familia: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    Familia_: Mapped[Optional['Familia']] = relationship('Familia', back_populates='Color')
    Componente: Mapped[List['Componente']] = relationship('Componente', back_populates='Color_')
    Producto_Simple: Mapped[List['ProductoSimple']] = relationship('ProductoSimple', back_populates='Color_')


class ComposicionPack(Base):
    __tablename__ = 'Composicion_Pack'
    __table_args__ = (
        ForeignKeyConstraint(['id_pack'], ['Pack.id'], ondelete='CASCADE', onupdate='CASCADE', name='Composicion_Pack_id_pack_fkey'),
        ForeignKeyConstraint(['id_producto'], ['Producto.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Composicion_Pack_id_producto_fkey'),
        PrimaryKeyConstraint('id_pack', 'id_producto', name='Composicion_Pack_pkey')
    )

    id_pack: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_producto: Mapped[int] = mapped_column(Integer, primary_key=True)
    cantidad: Mapped[int] = mapped_column(Integer, server_default=text('0'))

    Pack_: Mapped['Pack'] = relationship('Pack', back_populates='Composicion_Pack')
    Producto_: Mapped['Producto'] = relationship('Producto', back_populates='Composicion_Pack')


class Componente(Base):
    __tablename__ = 'Componente'
    __table_args__ = (
        ForeignKeyConstraint(['id_color'], ['Color.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Componente_id_color_fkey'),
        ForeignKeyConstraint(['id_proveedor'], ['Proveedor.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Componente_id_proveedor_fkey'),
        PrimaryKeyConstraint('id', name='Componente_pkey'),
        UniqueConstraint('nombre', name='Componente_nombre_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    id_proveedor: Mapped[Optional[int]] = mapped_column(Integer)
    id_color: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    Color_: Mapped[Optional['Color']] = relationship('Color', back_populates='Componente')
    Proveedor_: Mapped[Optional['Proveedor']] = relationship('Proveedor', back_populates='Componente')
    Composicion_Prod_Compuesto: Mapped[List['ComposicionProdCompuesto']] = relationship('ComposicionProdCompuesto', back_populates='Componente_')
    Stock: Mapped[List['Stock']] = relationship('Stock', back_populates='Componente_')


class ProductoSimple(Base):
    __tablename__ = 'Producto_Simple'
    __table_args__ = (
        CheckConstraint("tipo IS NULL OR (tipo::text = ANY (ARRAY['simple'::character varying, 'compuesto'::character varying, 'pack'::character varying]::text[]))", name='Articulo_tipo_check'),
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
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    id_proveedor: Mapped[Optional[int]] = mapped_column(Integer)
    id_color: Mapped[Optional[int]] = mapped_column(Integer)

    Color_: Mapped[Optional['Color']] = relationship('Color', back_populates='Producto_Simple')
    Proveedor_: Mapped[Optional['Proveedor']] = relationship('Proveedor', back_populates='Producto_Simple')
    Stock: Mapped[List['Stock']] = relationship('Stock', back_populates='Producto_Simple')


class ComposicionProdCompuesto(Base):
    __tablename__ = 'Composicion_Prod_Compuesto'
    __table_args__ = (
        ForeignKeyConstraint(['id_componente'], ['Componente.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Composicion_Prod_Compuesto_id_componente_fkey'),
        ForeignKeyConstraint(['id_producto_compuesto'], ['Producto_Compuesto.id'], ondelete='CASCADE', onupdate='CASCADE', name='Composicion_Prod_Compuesto_id_producto_compuesto_fkey'),
        PrimaryKeyConstraint('id_producto_compuesto', 'id_componente', name='Composicion_Prod_Compuesto_pkey')
    )

    id_producto_compuesto: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_componente: Mapped[int] = mapped_column(Integer, primary_key=True)
    cantidad: Mapped[Optional[int]] = mapped_column(Integer)

    Componente_: Mapped['Componente'] = relationship('Componente', back_populates='Composicion_Prod_Compuesto')
    Producto_Compuesto: Mapped['ProductoCompuesto'] = relationship('ProductoCompuesto', back_populates='Composicion_Prod_Compuesto')


class Stock(Base):
    __tablename__ = 'Stock'
    __table_args__ = (
        CheckConstraint("tipo::text = 'componente'::text AND id_componente IS NOT NULL AND id_producto_simple IS NULL OR tipo::text = 'producto_simple'::text AND id_producto_simple IS NOT NULL AND id_componente IS NULL", name='Stock_check'),
        CheckConstraint("tipo::text = ANY (ARRAY['producto_simple'::character varying, 'componente'::character varying]::text[])", name='Stock_tipo_check'),
        ForeignKeyConstraint(['id_componente'], ['Componente.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Stock_id_componente_fkey'),
        ForeignKeyConstraint(['id_producto_simple'], ['Producto_Simple.id'], ondelete='RESTRICT', onupdate='CASCADE', name='Stock_id_producto_simple_fkey'),
        PrimaryKeyConstraint('id', name='Stock_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    cantidad: Mapped[int] = mapped_column(Integer, server_default=text('0'))
    cantidad_minima: Mapped[int] = mapped_column(Integer, server_default=text('0'))
    tipo: Mapped[str] = mapped_column(String(31))
    ubicacion: Mapped[Optional[str]] = mapped_column(String(255))
    id_componente: Mapped[Optional[int]] = mapped_column(Integer)
    id_producto_simple: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    Componente_: Mapped[Optional['Componente']] = relationship('Componente', back_populates='Stock')
    Producto_Simple: Mapped[Optional['ProductoSimple']] = relationship('ProductoSimple', back_populates='Stock')
    Movimiento: Mapped[List['Movimiento']] = relationship('Movimiento', back_populates='Stock_')


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
