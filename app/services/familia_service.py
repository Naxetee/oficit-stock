"""
🏷️ Servicio de Familia - Gestión de familias de productos

Este servicio maneja todas las operaciones relacionadas con las familias
de productos, incluyendo operaciones CRUD y consultas específicas.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.familia import Familia
from app.models.articulo import Articulo
from app.models.color import Color
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class FamiliaService(BaseService):
    """
    🏷️ Servicio para gestión de familias de productos
    
    Maneja operaciones específicas de familias incluyendo:
    - CRUD básico de familias
    - Consultas de artículos por familia
    - Consultas de colores asociados a familia
    - Validaciones de negocio específicas
    """
    
    def __init__(self, db_session: Session):
        """
        Constructor del servicio de familias
        
        Args:
            db_session (Session): Sesión de base de datos SQLAlchemy
        """
        super().__init__(db_session, Familia)
        
    def crear_familia(self, nombre: str, descripcion: str = None) -> Familia:
        """
        Crear una nueva familia de productos
        
        Args:
            nombre (str): Nombre de la familia (requerido)
            descripcion (str, optional): Descripción de la familia
            
        Returns:
            Familia: Nueva familia creada
            
        Raises:
            ValueError: Si el nombre ya existe
            SQLAlchemyError: Error en la operación de base de datos
        """
        try:
            # Verificar que no exista una familia con el mismo nombre
            familia_existente = self.obtener_por_nombre(nombre)
            if familia_existente:
                raise ValueError(f"Ya existe una familia con el nombre '{nombre}'")
                
            familia = self.crear(nombre=nombre, descripcion=descripcion)
            logger.info(f"✅ Familia '{nombre}' creada exitosamente")
            return familia
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error creando familia '{nombre}': {e}")
            raise
            
    def obtener_por_nombre(self, nombre: str) -> Optional[Familia]:
        """
        Obtener una familia por su nombre
        
        Args:
            nombre (str): Nombre de la familia a buscar
            
        Returns:
            Optional[Familia]: Familia encontrada o None
        """
        try:
            return self.db.query(Familia).filter(Familia.nombre == nombre).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando familia por nombre '{nombre}': {e}")
            raise
            
    def obtener_articulos_por_familia(self, familia_id: int) -> List[Articulo]:
        """
        Obtener todos los artículos de una familia específica
        
        Args:
            familia_id (int): ID de la familia
            
        Returns:
            List[Articulo]: Lista de artículos de la familia
        """
        try:
            return self.db.query(Articulo).filter(Articulo.id_familia == familia_id).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo artículos de familia {familia_id}: {e}")
            raise
            
    def obtener_colores_por_familia(self, familia_id: int) -> List[Color]:
        """
        Obtener todos los colores asociados a una familia
        
        Args:
            familia_id (int): ID de la familia
            
        Returns:
            List[Color]: Lista de colores de la familia
        """
        try:
            return self.db.query(Color).filter(Color.id_familia == familia_id).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo colores de familia {familia_id}: {e}")
            raise
            
    def obtener_estadisticas_familia(self, familia_id: int) -> dict:
        """
        Obtener estadísticas de una familia específica
        
        Args:
            familia_id (int): ID de la familia
            
        Returns:
            dict: Estadísticas de la familia incluyendo:
                - total_articulos: Número de artículos
                - total_colores: Número de colores
                - familia_info: Información básica de la familia
        """
        try:
            familia = self.obtener_por_id(familia_id)
            if not familia:
                return {'error': 'Familia no encontrada'}
                
            total_articulos = len(self.obtener_articulos_por_familia(familia_id))
            total_colores = len(self.obtener_colores_por_familia(familia_id))
            
            return {
                'familia_info': {
                    'id': familia.id,
                    'nombre': familia.nombre,
                    'descripcion': familia.descripcion
                },
                'total_articulos': total_articulos,
                'total_colores': total_colores,
                'fecha_creacion': familia.created_at,
                'ultima_actualizacion': familia.updated_at
            }
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo estadísticas de familia {familia_id}: {e}")
            raise
            
    def buscar_familias_por_texto(self, texto: str) -> List[Familia]:
        """
        Buscar familias por texto en nombre o descripción
        
        Args:
            texto (str): Texto a buscar
            
        Returns:
            List[Familia]: Lista de familias que coinciden con la búsqueda
        """
        try:
            return self.db.query(Familia).filter(
                (Familia.nombre.ilike(f'%{texto}%')) |
                (Familia.descripcion.ilike(f'%{texto}%'))
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando familias por texto '{texto}': {e}")
            raise
            
    def validar_eliminacion(self, familia_id: int) -> dict:
        """
        Validar si una familia puede ser eliminada
        
        Args:
            familia_id (int): ID de la familia a validar
            
        Returns:
            dict: Resultado de la validación con:
                - puede_eliminar: bool
                - razon: str (si no puede eliminar)
                - elementos_relacionados: dict con conteos
        """
        try:
            articulos = self.obtener_articulos_por_familia(familia_id)
            colores = self.obtener_colores_por_familia(familia_id)
            
            puede_eliminar = len(articulos) == 0 and len(colores) == 0
            
            resultado = {
                'puede_eliminar': puede_eliminar,
                'elementos_relacionados': {
                    'articulos': len(articulos),
                    'colores': len(colores)
                }
            }
            
            if not puede_eliminar:
                resultado['razon'] = f"La familia tiene {len(articulos)} artículos y {len(colores)} colores asociados"
                
            return resultado
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error validando eliminación de familia {familia_id}: {e}")
            raise
