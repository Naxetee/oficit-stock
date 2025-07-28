"""
🔧 Servicio Base - Funcionalidades comunes para todos los servicios

Este módulo contiene la clase base con funcionalidades compartidas
por todos los servicios del sistema de inventario.
"""

from typing import Any, List, Optional, Type, TypeVar, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

# Type variable para el modelo genérico
ModelType = TypeVar('ModelType')

logger = logging.getLogger(__name__)


class BaseService:
    """
    🏗️ Clase base para todos los servicios del sistema
    
    Proporciona funcionalidades CRUD básicas y manejo de errores comunes
    que pueden ser reutilizadas por todos los servicios específicos.
    """
    
    def __init__(self, db_session: Session, model_class: Type[ModelType]):
        """
        Constructor del servicio base
        
        Args:
            db_session (Session): Sesión de base de datos SQLAlchemy
            model_class (Type[ModelType]): Clase del modelo asociado al servicio
        """
        self.db = db_session
        self.model_class = model_class
        
    def crear(self, **kwargs) -> ModelType:
        """
        Crear una nueva instancia del modelo
        
        Args:
            **kwargs: Campos del modelo a crear
            
        Returns:
            ModelType: Instancia creada
            
        Raises:
            SQLAlchemyError: Error en la operación de base de datos
        """
        try:
            instancia = self.model_class(**kwargs)
            self.db.add(instancia)
            self.db.commit()
            self.db.refresh(instancia)
            
            logger.info(f"✅ Creado {self.model_class.__name__} con ID: {instancia.id}")
            return instancia
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error creando {self.model_class.__name__}: {e}")
            raise
            
    def obtener_por_id(self, id: int) -> Optional[ModelType]:
        """
        Obtener una instancia por su ID
        
        Args:
            id (int): ID de la instancia a buscar
            
        Returns:
            Optional[ModelType]: Instancia encontrada o None
        """
        try:
            return self.db.query(self.model_class).filter(self.model_class.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo {self.model_class.__name__} con ID {id}: {e}")
            raise
            
    def obtener_todos(self, limite: Optional[int] = None, offset: int = 0) -> List[ModelType]:
        """
        Obtener todas las instancias del modelo
        
        Args:
            limite (Optional[int]): Límite de resultados
            offset (int): Número de registros a saltar
            
        Returns:
            List[ModelType]: Lista de instancias
        """
        try:
            query = self.db.query(self.model_class).offset(offset)
            if limite:
                query = query.limit(limite)
            return query.all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo todos los {self.model_class.__name__}: {e}")
            raise
            
    def actualizar(self, id: int, **kwargs) -> Optional[ModelType]:
        """
        Actualizar una instancia existente
        
        Args:
            id (int): ID de la instancia a actualizar
            **kwargs: Campos a actualizar
            
        Returns:
            Optional[ModelType]: Instancia actualizada o None si no existe
        """
        try:
            instancia = self.obtener_por_id(id)
            if not instancia:
                return None
                
            for campo, valor in kwargs.items():
                if hasattr(instancia, campo):
                    setattr(instancia, campo, valor)
                    
            self.db.commit()
            self.db.refresh(instancia)
            
            logger.info(f"✅ Actualizado {self.model_class.__name__} con ID: {id}")
            return instancia
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error actualizando {self.model_class.__name__} con ID {id}: {e}")
            raise
            
    def eliminar(self, id: int) -> bool:
        """
        Eliminar una instancia por su ID
        
        Args:
            id (int): ID de la instancia a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        try:
            instancia = self.obtener_por_id(id)
            if not instancia:
                return False
                
            self.db.delete(instancia)
            self.db.commit()
            
            logger.info(f"✅ Eliminado {self.model_class.__name__} con ID: {id}")
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Error eliminando {self.model_class.__name__} con ID {id}: {e}")
            raise
            
    def contar(self) -> int:
        """
        Contar el número total de instancias
        
        Returns:
            int: Número de instancias
        """
        try:
            return self.db.query(self.model_class).count()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error contando {self.model_class.__name__}: {e}")
            raise
            
    def buscar(self, filtros: Dict[str, Any]) -> List[ModelType]:
        """
        Buscar instancias por filtros específicos
        
        Args:
            filtros (Dict[str, Any]): Diccionario con campo -> valor a filtrar
            
        Returns:
            List[ModelType]: Lista de instancias que coinciden con los filtros
        """
        try:
            query = self.db.query(self.model_class)
            
            for campo, valor in filtros.items():
                if hasattr(self.model_class, campo):
                    query = query.filter(getattr(self.model_class, campo) == valor)
                    
            return query.all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando {self.model_class.__name__}: {e}")
            raise
