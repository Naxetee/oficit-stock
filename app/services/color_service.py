"""
🎨 Servicio de Color - Gestión de colores para productos y componentes

Este servicio maneja todas las operaciones relacionadas con los colores
disponibles para productos simples y componentes.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.color import Color
from app.models.familia import Familia
from app.models.producto_simple import ProductoSimple
from app.models.componente import Componente
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class ColorService(BaseService):
    """
    🎨 Servicio para gestión de colores
    
    Maneja operaciones específicas de colores incluyendo:
    - CRUD básico de colores
    - Asociación con familias
    - Consultas de productos por color
    - Validaciones de disponibilidad
    """
    
    def __init__(self, db_session: Session):
        """
        Constructor del servicio de colores
        
        Args:
            db_session (Session): Sesión de base de datos SQLAlchemy
        """
        super().__init__(db_session, Color)
        
    def crear_color(self, nombre: str, codigo_hex: str = None, url_imagen: str = None,
                    id_familia: int = None) -> Color:
        """
        Crear un nuevo color
        
        Args:
            nombre (str): Nombre del color (requerido)
            codigo_hex (str, optional): Código hexadecimal del color
            url_imagen (str, optional): URL de imagen representativa
            id_familia (int, optional): ID de la familia asociada
            
        Returns:
            Color: Nuevo color creado
            
        Raises:
            ValueError: Si la familia no existe
            SQLAlchemyError: Error en la operación de base de datos
        """
        try:
            # Validar que la familia existe si se proporciona
            if id_familia:
                familia = self.db.query(Familia).filter(Familia.id == id_familia).first()
                if not familia:
                    raise ValueError(f"La familia con ID {id_familia} no existe")
                    
            color = self.crear(
                nombre=nombre,
                codigo_hex=codigo_hex,
                url_imagen=url_imagen,
                id_familia=id_familia
            )
            
            logger.info(f"✅ Color '{nombre}' creado exitosamente")
            return color
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error creando color '{nombre}': {e}")
            raise
            
    def obtener_por_nombre(self, nombre: str) -> Optional[Color]:
        """
        Obtener un color por su nombre
        
        Args:
            nombre (str): Nombre del color a buscar
            
        Returns:
            Optional[Color]: Color encontrado o None
        """
        try:
            return self.db.query(Color).filter(Color.nombre == nombre).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando color por nombre '{nombre}': {e}")
            raise
            
    def obtener_por_familia(self, familia_id: int) -> List[Color]:
        """
        Obtener todos los colores de una familia específica
        
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
            
    def obtener_productos_por_color(self, color_id: int) -> List[ProductoSimple]:
        """
        Obtener todos los productos simples que usan un color específico
        
        Args:
            color_id (int): ID del color
            
        Returns:
            List[ProductoSimple]: Lista de productos simples con el color
        """
        try:
            return self.db.query(ProductoSimple).filter(
                ProductoSimple.id_color == color_id
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo productos por color {color_id}: {e}")
            raise
            
    def obtener_componentes_por_color(self, color_id: int) -> List[Componente]:
        """
        Obtener todos los componentes que usan un color específico
        
        Args:
            color_id (int): ID del color
            
        Returns:
            List[Componente]: Lista de componentes con el color
        """
        try:
            return self.db.query(Componente).filter(
                Componente.id_color == color_id
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo componentes por color {color_id}: {e}")
            raise
            
    def obtener_estadisticas_color(self, color_id: int) -> dict:
        """
        Obtener estadísticas de uso de un color específico
        
        Args:
            color_id (int): ID del color
            
        Returns:
            dict: Estadísticas del color incluyendo:
                - color_info: Información básica del color
                - total_productos: Número de productos que lo usan
                - total_componentes: Número de componentes que lo usan
                - familia_asociada: Información de la familia
        """
        try:
            color = self.obtener_por_id(color_id)
            if not color:
                return {'error': 'Color no encontrado'}
                
            productos = self.obtener_productos_por_color(color_id)
            componentes = self.obtener_componentes_por_color(color_id)
            
            familia_info = None
            if color.id_familia:
                familia = self.db.query(Familia).filter(Familia.id == color.id_familia).first()
                if familia:
                    familia_info = {
                        'id': familia.id,
                        'nombre': familia.nombre
                    }
                    
            return {
                'color_info': {
                    'id': color.id,
                    'nombre': color.nombre,
                    'codigo_hex': color.codigo_hex,
                    'url_imagen': color.url_imagen
                },
                'total_productos': len(productos),
                'total_componentes': len(componentes),
                'familia_asociada': familia_info,
                'fecha_creacion': color.created_at,
                'ultima_actualizacion': color.updated_at
            }
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo estadísticas de color {color_id}: {e}")
            raise
            
    def buscar_colores_por_texto(self, texto: str) -> List[Color]:
        """
        Buscar colores por texto en nombre
        
        Args:
            texto (str): Texto a buscar
            
        Returns:
            List[Color]: Lista de colores que coinciden con la búsqueda
        """
        try:
            return self.db.query(Color).filter(
                Color.nombre.ilike(f'%{texto}%')
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando colores por texto '{texto}': {e}")
            raise
            
    def validar_eliminacion(self, color_id: int) -> dict:
        """
        Validar si un color puede ser eliminado
        
        Args:
            color_id (int): ID del color a validar
            
        Returns:
            dict: Resultado de la validación con:
                - puede_eliminar: bool
                - razon: str (si no puede eliminar)
                - elementos_relacionados: dict con conteos
        """
        try:
            productos = self.obtener_productos_por_color(color_id)
            componentes = self.obtener_componentes_por_color(color_id)
            
            puede_eliminar = len(productos) == 0 and len(componentes) == 0
            
            resultado = {
                'puede_eliminar': puede_eliminar,
                'elementos_relacionados': {
                    'productos': len(productos),
                    'componentes': len(componentes)
                }
            }
            
            if not puede_eliminar:
                resultado['razon'] = f"El color está siendo usado por {len(productos)} productos y {len(componentes)} componentes"
                
            return resultado
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error validando eliminación de color {color_id}: {e}")
            raise
            
    def obtener_colores_disponibles_para_familia(self, familia_id: int) -> List[Color]:
        """
        Obtener colores disponibles para una familia específica
        (incluyendo colores sin familia asignada)
        
        Args:
            familia_id (int): ID de la familia
            
        Returns:
            List[Color]: Lista de colores disponibles
        """
        try:
            return self.db.query(Color).filter(
                (Color.id_familia == familia_id) | (Color.id_familia.is_(None))
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo colores disponibles para familia {familia_id}: {e}")
            raise
