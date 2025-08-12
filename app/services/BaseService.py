from fastapi import HTTPException
from typing import Type, TypeVar, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)

class BaseService:
    """
    Clase base de servicio que proporciona operaciones CRUD comunes para modelos de SQLAlchemy.
    Esta clase puede ser extendida para crear servicios específicos para diferentes modelos.
    Incluye métodos para:
    - obtener_todos: Recuperar todos los registros con filtros opcionales.
    - obtener_por_id: Recuperar un registro por su ID.
    - crear: Crear un nuevo registro.
    - actualizar: Actualizar un registro existente por ID.
    - eliminar: Eliminar un registro por ID.
    """
    def __init__(self, db: Session, model: Type[ModelType], response_schema: Type[ResponseSchemaType]):
        """
        Inicializa el servicio con una sesión de base de datos, un modelo y un esquema de respuesta.
        Args:
            db (Session): La sesión de base de datos SQLAlchemy.
            model (Type[ModelType]): El modelo SQLAlchemy que este servicio manejará.
            response_schema (Type[ResponseSchemaType]): El esquema Pydantic para la respuesta.      
        """
        self.db = db
        self.model = model
        self.response_schema = response_schema

    def obtener_todos(self, skip: int = 0, limit: int = 100, filtros: Optional[Dict[str, Any]] = None) -> List[ResponseSchemaType]:
        """
        Recupera todos los registros del modelo, aplicando filtros opcionales.
        Args:
            filtros (Optional[Dict[str, Any]]): Un diccionario de filtros para aplicar a la consulta.
        Returns:
            List[ResponseSchemaType]: Una lista de objetos del esquema de respuesta.
        """
        query = select(self.model)
        if filtros:
            for attr, value in filtros.items():
                if hasattr(self.model, attr) and value is not None:
                    column = getattr(self.model, attr)
                    # Solo usar ilike para strings, comparación directa para otros tipos
                    if isinstance(value, str):
                        query = query.where(column.ilike(f"%{value}%"))
                    else:
                        query = query.where(column == value)
        result = self.db.scalars(query.offset(skip).limit(limit))
        return result.all()

    def obtener_por_id(self, id: Any) -> Optional[ResponseSchemaType]:
        """
        Recupera un registro por su ID.
        Args:
            id (Any): El ID del registro a recuperar.
        Returns:
            Optional[ResponseSchemaType]: Un objeto del esquema de respuesta si se encuentra el registro, de lo contrario None.
        """
        obj = self.db.get(self.model, id)
        if obj:
            return obj
        return None

    def crear(self, entidad_create: CreateSchemaType) -> ResponseSchemaType:
        """
        Crea un nuevo registro en la base de datos.
        Args:
            entidad_create (CreateSchemaType): Un objeto del esquema de creación que contiene los datos para el nuevo registro.
        Returns:
            ResponseSchemaType: Un objeto del esquema de respuesta que representa el registro creado.
        """
        try:
            obj = self.model(**entidad_create.model_dump())
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"No se pudo crear {self.model.__name__} por restricción de clave o integridad")
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error inesperado al crear {self.model.__name__}: {str(e)}")

    def actualizar(self, id: Any, entidad_update: UpdateSchemaType) -> Optional[ResponseSchemaType]:
        """
        Actualiza un registro existente por ID.
        Args:
            id (Any): El ID del registro a actualizar.
            entidad_update (UpdateSchemaType): Un objeto del esquema de actualización que contiene los datos a modificar.
        Returns:
            Optional[ResponseSchemaType]: Un objeto del esquema de respuesta actualizado si se encuentra el registro, de lo contrario None.
        """
        obj = self.db.get(self.model, id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} id no encontrado")
        try:
            for key, value in entidad_update.model_dump(exclude_unset=True).items():
                setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"No se pudo actualizar {self.model.__name__} id={id} por restricción de clave o integridad")
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error inesperado al actualizar {self.model.__name__} id={id}: {str(e)}")

    def eliminar(self, id: Any) -> Dict[str, str]:
        """
        Elimina un registro por ID.
        Args:
            id (Any): El ID del registro a eliminar.
        Returns:
            Dict[str, str]: Un diccionario con un mensaje de éxito o error.
        """
        obj = self.db.get(self.model, id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} id no encontrado")
        try:
            self.db.delete(obj)
            self.db.commit()
            return {"detail": f"{self.model.__name__} id eliminado exitosamente"}
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"No se puede eliminar {self.model.__name__} id={id} por restricción de clave foránea")
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Error inesperado al eliminar {self.model.__name__} id={id}: {str(e)}")

    def contar(self) -> int:
        """
        Cuenta el número total de registros del modelo.
        Returns:
            int: El número total de registros.
        """
        return self.db.query(self.model).count()