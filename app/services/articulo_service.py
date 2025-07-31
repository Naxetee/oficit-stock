"""
📋 Servicio de Artículo - Gestión de artículos del inventario

Este servicio maneja todas las operaciones relacionadas con los artículos,
que son la entidad central que puede ser tanto productos como packs.
"""

from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.articulo import Articulo
from app.models.familia import Familia
from app.models.producto import Producto
from app.models.pack import Pack
from app.schemas.articuloDTO import ArticuloCreate, ArticuloResponse, ArticuloUpdate
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class ArticuloService(BaseService):
    """
    📋 Servicio para gestión de artículos
    
    Maneja operaciones específicas de artículos incluyendo:
    - CRUD básico de artículos
    - Relación polimórfica con productos y packs
    - Consultas por familia
    - Validaciones de negocio específicas
    """
    
    def __init__(self, db_session: Session):
        """
        Constructor del servicio de artículos
        
        Args:
            db_session (Session): Sesión de base de datos SQLAlchemy
        """
        super().__init__(db_session, Articulo)
        
    def crear_articulo( self, nuevo_articulo: ArticuloCreate) -> ArticuloResponse:
        """
        Crear un nuevo artículo con validaciones
        
        Args:
            nuevo_articulo (ArticuloCreate): Datos del artículo a crear
        Returns:
            articulo (ArticuloResponse): Artículo creado
        Raises:
            ValueError: Si hay errores de validación
            SQLAlchemyError: Error en la operación de base de datos
        """
        try:
            # Validar que la familia existe
            id_familia = nuevo_articulo.id_familia
            if id_familia:
                familia = self.db.query(Familia).filter(Familia.id == id_familia).first()
                if not familia:
                    raise ValueError(f"La familia con ID {id_familia} no existe")

            codigo = nuevo_articulo.codigo     
            # Validar que el código sea único si se proporciona
            if codigo:
                articulo_existente = self.obtener_por_codigo(codigo)
                if articulo_existente:
                    raise ValueError(f"Ya existe un artículo con el código '{codigo}'")
                    
            articulo = self.crear(**nuevo_articulo.model_dump())
            
            logger.info(f"✅ Artículo '{articulo.nombre}' creado exitosamente")
            return articulo
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error creando artículo '{articulo.nombre}': {e}")
            raise
            
    def obtener_por_nombre(self, nombre: str) -> Optional[ArticuloResponse]:
        """
        Obtener un artículo por su nombre
        
        Args:
            nombre (str): Nombre del artículo a buscar
            
        Returns:
            Optional[ArticuloResponse]: Artículo encontrado o None
        """
        try:
            return self.db.query(Articulo).filter(Articulo.nombre == nombre).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando artículo por nombre '{nombre}': {e}")
            raise
            
    def obtener_por_codigo(self, codigo: str) -> Optional[ArticuloResponse]:
        """
        Obtener un artículo por su código
        
        Args:
            codigo (str): Código del artículo a buscar
            
        Returns:
            Optional[ArticuloResponse]: Artículo encontrado o None
        """
        try:
            return self.db.query(Articulo).filter(Articulo.codigo == codigo).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando artículo por código '{codigo}': {e}")
            raise
            
    def obtener_por_familia(self, familia_id: int) -> List[ArticuloResponse]:
        """
        Obtener todos los artículos de una familia específica
        
        Args:
            familia_id (int): ID de la familia
            
        Returns:
            List[ArticuloResponse]: Lista de artículos de la familia
        """
        try:
            return self.db.query(Articulo).filter(Articulo.id_familia == familia_id).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo artículos de familia {familia_id}: {e}")
            raise
        
            
    def obtener_producto_asociado(self, articulo_id: int) -> Optional[Producto]:
        """
        Obtener el producto asociado a un artículo (relación polimórfica)
        
        Args:
            articulo_id (int): ID del artículo
            
        Returns:
            Optional[Producto]: Producto asociado o None
        """
        try:
            return self.db.query(Producto).filter(Producto.id_articulo == articulo_id).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo producto de artículo {articulo_id}: {e}")
            raise
            
    def obtener_pack_asociado(self, articulo_id: int) -> Optional[Pack]:
        """
        Obtener el pack asociado a un artículo (relación polimórfica)
        
        Args:
            articulo_id (int): ID del artículo
            
        Returns:
            Optional[Pack]: Pack asociado o None
        """
        try:
            return self.db.query(Pack).filter(Pack.id_articulo == articulo_id).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo pack de artículo {articulo_id}: {e}")
            raise
            
    def obtener_tipo_articulo(self, articulo_id: int) -> Optional[str]:
        """
        Determinar el tipo de artículo (producto o pack)
        
        Args:
            articulo_id (int): ID del artículo
            
        Returns:
            Optional[str]: 'producto', 'pack' o None si no existe
        """
        try:
            producto = self.obtener_producto_asociado(articulo_id)
            if producto:
                return 'producto'
                
            pack = self.obtener_pack_asociado(articulo_id)
            if pack:
                return 'pack'
                
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error determinando tipo de artículo {articulo_id}: {e}")
            raise
            
    def obtener_estadisticas_articulo(self, articulo_id: int) -> Dict[str, Any]:
        """
        Obtener estadísticas completas de un artículo
        
        Args:
            articulo_id (int): ID del artículo
            
        Returns:
            Dict[str, Any]: Estadísticas del artículo incluyendo:
                - articulo_info: Información básica
                - tipo: Tipo de artículo (producto/pack)
                - familia_info: Información de la familia
        """
        try:
            articulo = self.obtener_por_id(articulo_id)
            if not articulo:
                return {'error': 'Artículo no encontrado'}
                
            # Información básica del artículo
            resultado = {
                'articulo_info': {
                    'id': articulo.id,
                    'nombre': articulo.nombre,
                    'descripcion': articulo.descripcion,
                    'codigo': articulo.codigo,
                    'activo': articulo.activo,
                },
                'tipo': self.obtener_tipo_articulo(articulo_id),
                'fecha_creacion': articulo.created_at,
                'ultima_actualizacion': articulo.updated_at
            }
            
            # Información de la familia
            if articulo.id_familia:
                familia = self.db.query(Familia).filter(Familia.id == articulo.id_familia).first()
                if familia:
                    resultado['familia_info'] = {
                        'id': familia.id,
                        'nombre': familia.nombre,
                        'descripcion': familia.descripcion
                    }
                    
            return resultado
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo estadísticas de artículo {articulo_id}: {e}")
            raise
            
    def buscar_articulos_por_texto(self, texto: str) -> List[ArticuloResponse]:
        """
        Buscar artículos por texto en nombre, descripción o código
        
        Args:
            texto (str): Texto a buscar
            
        Returns:
            List[ArticuloResponse]: Lista de artículos que coinciden con la búsqueda
        """
        try:
            return self.db.query(Articulo).filter(
                (Articulo.nombre.ilike(f'%{texto}%')) |
                (Articulo.descripcion.ilike(f'%{texto}%')) |
                (Articulo.codigo.ilike(f'%{texto}%'))
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando artículos por texto '{texto}': {e}")
            raise
            
    def validar_eliminacion(self, articulo_id: int) -> Dict[str, Any]:
        """
        Validar si un artículo puede ser eliminado
        
        Args:
            articulo_id (int): ID del artículo a validar
            
        Returns:
            Dict[str, Any]: Resultado de la validación con:
                - puede_eliminar: bool
                - razon: str (si no puede eliminar)
                - elementos_relacionados: dict con información
        """
        try:
            producto = self.obtener_producto_asociado(articulo_id)
            pack = self.obtener_pack_asociado(articulo_id)
            
            tiene_relaciones = producto is not None or pack is not None
            
            resultado = {
                'puede_eliminar': not tiene_relaciones,
                'elementos_relacionados': {
                    'tiene_producto': producto is not None,
                    'tiene_pack': pack is not None
                }
            }
            
            if tiene_relaciones:
                elementos = []
                if producto:
                    elementos.append('producto')
                if pack:
                    elementos.append('pack')
                resultado['razon'] = f"El artículo tiene asociado: {', '.join(elementos)}"
                
            return resultado
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error validando eliminación de artículo {articulo_id}: {e}")
            raise
            
    def actualizar_articulo(self, articulo_id: int, articulo_actualizado: ArticuloUpdate) -> Optional[ArticuloResponse]:
        """
        Actualizar un artículo con validaciones
        
        Args:
            articulo_id (int): ID del artículo a actualizar
            articulo_actualizado (ArticuloUpdate): Datos actualizados del artículo
            
        Returns:
            Optional[ArticuloResponse]: Artículo actualizado o None si no existe
            
        Raises:
            ValueError: Si hay errores de validación
        """
        try:
            # Verificar si el artículo existe
            articulo_existente = self.obtener_por_id(articulo_id)
            if not articulo_existente:
                raise HTTPException(
                    status_code=404,
                    detail="Artículo no encontrado"
                )
                
            # Validaciones si se proporcionan estos campos
            id_familia = articulo_actualizado.id_familia
            if id_familia:
                familia = self.db.query(Familia).filter(Familia.id == id_familia).first()
                if not familia:
                    raise ValueError(f"La familia con ID {id_familia} no existe")

            codigo = articulo_actualizado.codigo      
            if codigo:
                codigo_existente = self.obtener_por_codigo(codigo)
                if codigo_existente and codigo_existente.id != articulo_id:
                    raise ValueError(f"Ya existe otro artículo con el código '{codigo}'")
 
            for key, value in articulo_actualizado.model_dump().items():
                setattr(articulo_existente, key, value)

            self.db.commit()
            self.db.refresh(articulo_existente)

            logger.info(f"✅ Artículo {articulo_id} actualizado exitosamente")
            return articulo_existente
            
        except ValueError:
            raise
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            logger.error(f"❌ Error actualizando artículo {articulo_id}: {e}")
            raise
