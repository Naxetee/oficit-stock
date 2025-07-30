"""
🏷️ Servicio de Familia - Gestión de familias de productos

Este servicio maneja todas las operaciones relacionadas con las familias
de productos, incluyendo operaciones CRUD y consultas específicas.
"""

from typing import List, Optional
from pydantic_core import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.familia import Familia
from app.models.articulo import Articulo
from app.models.color import Color
from app.schemas.articuloDTO import ArticuloInDB
from app.schemas.familiaDTO import FamiliaCreate, FamiliaResponse, FamiliaUpdate
from app.schemas.colorDTO import ColorInDB
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
        
    def crear_familia(self, nueva_familia : FamiliaCreate) -> FamiliaResponse:
        """
        Crear una nueva familia de productos
        
        Args:
            nueva_familia (FamiliaCreate): Datos de la nueva familia
            
        Returns:
            Familia: Nueva familia creada
            
        Raises:
            ValueError: Si el nombre ya existe
            SQLAlchemyError: Error en la operación de base de datos
        """
        try:
            nombre = nueva_familia.nombre
            # Verificar que no exista una familia con el mismo nombre
            familia_existente = self.obtener_por_nombre(nombre)
            if familia_existente:
                raise ValueError(f"Ya existe una familia con el nombre '{nombre}'")
                
            familia = self.crear(**nueva_familia.model_dump())
        except SQLAlchemyError as e:
            logger.error(f"❌ Error creando familia '{nombre}': {e}")
            raise

        try:
            # Convertir a FamiliaResponse antes de retornar
            logger.info(f"✅ Familia '{nombre}' creada exitosamente")
            return FamiliaResponse.model_validate(familia)
        except ValidationError as e:
            logger.error(f"❌ Error validando familia creada: {e}")
            raise
            
    def obtener_por_nombre(self, nombre: str) -> Optional[FamiliaResponse]:
        """
        Obtener una familia por su nombre
        
        Args:
            nombre (str): Nombre de la familia a buscar
            
        Returns:
            Optional[FamiliaResponse]: Familia encontrada o None
        """
        try:
            familia = self.db.query(Familia).filter(Familia.nombre.ilike(nombre)).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando familia por nombre '{nombre}': {e}")
            raise

        if familia:
            try:
                return FamiliaResponse.model_validate(familia)
            except ValidationError as e:
                logger.error(f"❌ Error validando familia '{nombre}': {e}")
                raise
        else:
            return None
            
    def obtener_articulos_por_familia(self, familia_id: int) -> List[ArticuloInDB]:
        """
        Obtener todos los artículos de una familia específica
        
        Args:
            familia_id (int): ID de la familia
            
        Returns:
            List[ArticuloInDB]: Lista de artículos de la familia
        """
        try:
            articulos = self.db.query(Articulo).filter(Articulo.id_familia == familia_id).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo artículos de familia {familia_id}: {e}")
            raise

        if not articulos:
            return []
        else:
            try:
                return [ArticuloInDB.model_validate(articulo) for articulo in articulos]
            except ValidationError as e:
                logger.error(f"❌ Error validando artículos de familia {familia_id}: {e}")
                raise
            
    def obtener_colores_por_familia(self, familia_id: int) -> List[ColorInDB]:
        """
        Obtener todos los colores asociados a una familia
        
        Args:
            familia_id (int): ID de la familia
            
        Returns:
            List[ColorInDB]: Lista de colores de la familia
        """
        try:
            colores = self.db.query(Color).filter(Color.id_familia == familia_id).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo colores de familia {familia_id}: {e}")
            raise
        if not colores:
            return []
        else:
            try:
                return [ColorInDB.model_validate(color) for color in colores]
            except ValidationError as e:
                logger.error(f"❌ Error validando colores de familia {familia_id}: {e}")
                raise
            
    def obtener_estadisticas_familia(self, familia_id: int) -> Optional[dict]:
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
                return None
                
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
            
    def buscar_familias_por_texto(self, texto: str) -> List[FamiliaResponse]:
        """
        Buscar familias por texto en nombre o descripción
        
        Args:
            texto (str): Texto a buscar
            
        Returns:
            List[FamiliaResponse]: Lista de familias que coinciden con la búsqueda
        """
        try:
            familias = self.db.query(Familia).filter(
                (Familia.nombre.ilike(f'%{texto}%')) |
                (Familia.descripcion.ilike(f'%{texto}%'))
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando familias por texto '{texto}': {e}")
            raise
        if not familias:
            return []
        else:
            try:
                return [FamiliaResponse.model_validate(familia) for familia in familias]
            except ValidationError as e:
                logger.error(f"❌ Error validando familias por texto '{texto}': {e}")
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
    
    def actualizar_familia(self, familia_id: int, datos_actualizacion: FamiliaUpdate) -> FamiliaResponse:
        """
        Actualizar una familia específica con validación
        
        Args:
            familia_id (int): ID de la familia a actualizar
            datos_actualizacion (FamiliaUpdate): Datos a actualizar
            
        Returns:
            FamiliaResponse: Familia actualizada
            
        Raises:
            ValueError: Si la familia no existe
            SQLAlchemyError: Error en la operación de base de datos
        """
        try:
            # Verificar que la familia existe
            familia_existente = self.db.query(Familia).filter(Familia.id == familia_id).first()
            if not familia_existente:
                raise ValueError(f"No se encontró familia con ID {familia_id}")

            datos_dict = datos_actualizacion.model_dump()
                        
            # Si se está actualizando el nombre, verificar que no existe otra familia con ese nombre
            familia_con_mismo_nombre = self.db.query(Familia).filter(
                Familia.nombre == datos_dict['nombre'],
                Familia.id != familia_id
            ).first()
            if familia_con_mismo_nombre:
                raise ValueError(f"Ya existe una familia con el nombre '{datos_dict['nombre']}'")
            
            # Actualizar los campos
            for campo, valor in datos_dict.items():
                setattr(familia_existente, campo, valor)
            
            # Guardar cambios
            self.db.commit()
            self.db.refresh(familia_existente)
            
            logger.info(f"✅ Familia ID {familia_id} actualizada exitosamente")
            return familia_existente
            
        except ValueError:
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error actualizando familia {familia_id}: {e}")
            raise
