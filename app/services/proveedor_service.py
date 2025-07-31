"""
🏪 Servicio de Proveedor - Gestión de proveedores de productos y componentes

Este servicio maneja todas las operaciones relacionadas con los proveedores,
incluyendo validaciones de datos y consultas de productos suministrados.
"""

from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.proveedor import Proveedor
from app.models.producto_simple import ProductoSimple
from app.models.componente import Componente
from app.schemas.componenteDTO import ComponenteResponse
from app.schemas.proveedorDTO import ProveedorCreate, ProveedorResponse, ProveedorUpdate
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class ProveedorService(BaseService):
    """
    🏪 Servicio para gestión de proveedores
    
    Maneja operaciones específicas de proveedores incluyendo:
    - CRUD básico de proveedores
    - Validaciones de NIF/CIF y email
    - Consultas de productos/componentes suministrados
    - Estadísticas de proveedores
    """
    
    def __init__(self, db_session: Session):
        """
        Constructor del servicio de proveedores
        
        Args:
            db_session (Session): Sesión de base de datos SQLAlchemy
        """
        super().__init__(db_session, Proveedor)
        
    def crear_proveedor(self, nuevo_proveedor : ProveedorCreate) -> ProveedorResponse:
        """
        Crear un nuevo proveedor con validaciones
        
        Args:
            nuevo_proveedor (ProveedorCreate): Datos del nuevo proveedor
        Returns:
            Proveedor (ProveedorResponse): Nuevo proveedor creado
            
        Raises:
            ValueError: Si hay errores de validación
            SQLAlchemyError: Error en la operación de base de datos
        """
        try:
            nif_cif = nuevo_proveedor.nif_cif
            nombre = nuevo_proveedor.nombre
            # Verificar que no exista un proveedor con el mismo NIF/CIF
            if nif_cif and self.obtener_por_nif_cif(nif_cif):
                raise ValueError(f"Ya existe un proveedor con NIF/CIF '{nif_cif}'")

            if self.obtener_por_nombre(nombre):
                raise ValueError(f"Ya existe un proveedor con nombre '{nombre}'")
                    
            proveedor = self.crear(**nuevo_proveedor.model_dump())
            
            logger.info(f"✅ Proveedor '{nuevo_proveedor.nombre}' creado exitosamente")
            return proveedor
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error creando proveedor '{nuevo_proveedor.nombre}': {e}")
            raise
            
    def obtener_por_nombre(self, nombre: str) -> Optional[ProveedorResponse]:
        """
        Obtener un proveedor por su nombre
        
        Args:
            nombre (str): Nombre del proveedor a buscar
            
        Returns:
            Optional[ProveedorResponse]: Proveedor encontrado o None
        """
        try:
            return self.db.query(Proveedor).filter(Proveedor.nombre == nombre).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando proveedor por nombre '{nombre}': {e}")
            raise
            
    def obtener_por_nif_cif(self, nif_cif: str) -> Optional[ProveedorResponse]:
        """
        Obtener un proveedor por su NIF/CIF
        
        Args:
            nif_cif (str): NIF/CIF del proveedor a buscar
            
        Returns:
            Optional[ProveedorResponse]: Proveedor encontrado o None
        """
        try:
            return self.db.query(Proveedor).filter(Proveedor.nif_cif == nif_cif).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando proveedor por NIF/CIF '{nif_cif}': {e}")
            raise
            
    def obtener_productos_suministrados(self, proveedor_id: int) -> List[ProductoSimple]:
        """
        Obtener todos los productos simples suministrados por un proveedor
        
        Args:
            proveedor_id (int): ID del proveedor
            
        Returns:
            List[ProductoSimple]: Lista de productos suministrados
        """
        try:
            return self.db.query(ProductoSimple).filter(
                ProductoSimple.id_proveedor == proveedor_id
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo productos de proveedor {proveedor_id}: {e}")
            raise
            
    def obtener_componentes_suministrados(self, proveedor_id: int) -> List[ComponenteResponse]:
        """
        Obtener todos los componentes suministrados por un proveedor
        
        Args:
            proveedor_id (int): ID del proveedor
            
        Returns:
            List[ComponenteResponse]: Lista de componentes suministrados
        """
        try:
            return self.db.query(Componente).filter(
                Componente.id_proveedor == proveedor_id
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo componentes de proveedor {proveedor_id}: {e}")
            raise
            
    def obtener_estadisticas_proveedor(self, proveedor_id: int) -> dict:
        """
        Obtener estadísticas de un proveedor específico
        
        Args:
            proveedor_id (int): ID del proveedor
            
        Returns:
            dict: Estadísticas del proveedor incluyendo:
                - proveedor_info: Información básica del proveedor
                - total_productos: Número de productos suministrados
                - total_componentes: Número de componentes suministrados
        """
        try:
            proveedor = self.obtener_por_id(proveedor_id)
            if not proveedor:
                return {'error': 'Proveedor no encontrado'}
                
            productos = self.obtener_productos_suministrados(proveedor_id)
            componentes = self.obtener_componentes_suministrados(proveedor_id)
            
            return {
                'proveedor_info': {
                    'id': proveedor.id,
                    'nombre': proveedor.nombre,
                    'nif_cif': proveedor.nif_cif,
                    'direccion': proveedor.direccion,
                    'telefono': proveedor.telefono,
                    'email': proveedor.email
                },
                'total_productos': len(productos),
                'total_componentes': len(componentes),
                'total_elementos': len(productos) + len(componentes),
                'fecha_creacion': proveedor.created_at,
                'ultima_actualizacion': proveedor.updated_at
            }
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error obteniendo estadísticas de proveedor {proveedor_id}: {e}")
            raise
            
    def buscar_proveedores_por_texto(self, texto: str) -> List[ProveedorResponse]:
        """
        Buscar proveedores por texto en nombre, NIF/CIF o email
        
        Args:
            texto (str): Texto a buscar
            
        Returns:
            List[ProveedorResponse]: Lista de proveedores que coinciden con la búsqueda
        """
        try:
            return self.db.query(Proveedor).filter(
                (Proveedor.nombre.ilike(f'%{texto}%')) |
                (Proveedor.nif_cif.ilike(f'%{texto}%')) |
                (Proveedor.email.ilike(f'%{texto}%'))
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando proveedores por texto '{texto}': {e}")
            raise
            
    def validar_eliminacion(self, proveedor_id: int) -> dict:
        """
        Validar si un proveedor puede ser eliminado
        
        Args:
            proveedor_id (int): ID del proveedor a validar
            
        Returns:
            dict: Resultado de la validación con:
                - puede_eliminar: bool
                - razon: str (si no puede eliminar)
                - elementos_relacionados: dict con conteos
        """
        try:
            productos = self.obtener_productos_suministrados(proveedor_id)
            componentes = self.obtener_componentes_suministrados(proveedor_id)
            
            puede_eliminar = len(productos) == 0 and len(componentes) == 0
            
            resultado = {
                'puede_eliminar': puede_eliminar,
                'elementos_relacionados': {
                    'productos': len(productos),
                    'componentes': len(componentes)
                }
            }
            
            if not puede_eliminar:
                resultado['razon'] = f"El proveedor suministra {len(productos)} productos y {len(componentes)} componentes"
                
            return resultado
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error validando eliminación de proveedor {proveedor_id}: {e}")
            raise
        
    def actualizar_proveedor(self, proveedor_id: int, proveedor: ProveedorUpdate) -> Optional[ProveedorResponse]:
        """
        Actualizar un proveedor con validaciones
        
        Args:
            proveedor_id (int): ID del proveedor a actualizar
            **kwargs: Campos a actualizar
            
        Returns:
            Optional[Proveedor]: Proveedor actualizado o None si no existe
            
        Raises:
            ValueError: Si hay errores de validación
        """
        try:
            existing_proveedor = self.obtener_por_id(proveedor_id)
            if not existing_proveedor:
                raise HTTPException(
                    status_code=404,
                    detail="Proveedor no encontrado"
                )
            
            # Verificar que no exista otro proveedor con el mismo NIF/CIF
            nif_cif = proveedor.nif_cif
            nombre = proveedor.nombre
            proveedor_existente = self.obtener_por_nif_cif(nif_cif)
            if proveedor_existente and proveedor_existente.id != proveedor_id:
                raise ValueError(f"Ya existe otro proveedor con NIF/CIF '{nif_cif}'")
            proveedor_existente = self.obtener_por_nombre(nombre)
            if proveedor_existente and proveedor_existente.id != proveedor_id:
                raise ValueError(f"Ya existe otro proveedor con nombre '{nombre}'")
            
            # Actualizar los campos del color
            for key, value in proveedor.model_dump().items():
                setattr(existing_proveedor, key, value)  

            self.db.commit()
            self.db.refresh(existing_proveedor)

            logger.info(f"✅ Proveedor {proveedor_id} actualizado exitosamente")
            return existing_proveedor
            
        except ValueError:
            raise
        except SQLAlchemyError as e:
            logger.error(f"❌ Error actualizando proveedor '{proveedor_id}': {e}")
            raise HTTPException(status_code=500, detail=f"Error al actualizar proveedor: {str(e)}")
