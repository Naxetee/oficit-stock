"""
🏪 Servicio de Proveedor - Gestión de proveedores de productos y componentes

Este servicio maneja todas las operaciones relacionadas con los proveedores,
incluyendo validaciones de datos y consultas de productos suministrados.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import re

from app.models.proveedor import Proveedor
from app.models.producto_simple import ProductoSimple
from app.models.componente import Componente
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
        
    def crear_proveedor(self, nombre: str, nif_cif: str = None, 
                       direccion: str = None, telefono: str = None, 
                       email: str = None) -> Proveedor:
        """
        Crear un nuevo proveedor con validaciones
        
        Args:
            nombre (str): Nombre del proveedor (requerido)
            nif_cif (str, optional): NIF o CIF del proveedor
            direccion (str, optional): Dirección del proveedor
            telefono (str, optional): Teléfono de contacto
            email (str, optional): Email de contacto
            
        Returns:
            Proveedor: Nuevo proveedor creado
            
        Raises:
            ValueError: Si hay errores de validación
            SQLAlchemyError: Error en la operación de base de datos
        """
        try:
            # Validaciones de datos
            if nif_cif and not self._validar_nif_cif(nif_cif):
                raise ValueError(f"El NIF/CIF '{nif_cif}' no tiene un formato válido")
                
            if email and not self._validar_email(email):
                raise ValueError(f"El email '{email}' no tiene un formato válido")
                
            # Verificar que no exista un proveedor con el mismo NIF/CIF
            if nif_cif:
                proveedor_existente = self.obtener_por_nif_cif(nif_cif)
                if proveedor_existente:
                    raise ValueError(f"Ya existe un proveedor con NIF/CIF '{nif_cif}'")
                    
            proveedor = self.crear(
                nombre=nombre,
                nif_cif=nif_cif,
                direccion=direccion,
                telefono=telefono,
                email=email
            )
            
            logger.info(f"✅ Proveedor '{nombre}' creado exitosamente")
            return proveedor
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error creando proveedor '{nombre}': {e}")
            raise
            
    def obtener_por_nombre(self, nombre: str) -> Optional[Proveedor]:
        """
        Obtener un proveedor por su nombre
        
        Args:
            nombre (str): Nombre del proveedor a buscar
            
        Returns:
            Optional[Proveedor]: Proveedor encontrado o None
        """
        try:
            return self.db.query(Proveedor).filter(Proveedor.nombre == nombre).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Error buscando proveedor por nombre '{nombre}': {e}")
            raise
            
    def obtener_por_nif_cif(self, nif_cif: str) -> Optional[Proveedor]:
        """
        Obtener un proveedor por su NIF/CIF
        
        Args:
            nif_cif (str): NIF/CIF del proveedor a buscar
            
        Returns:
            Optional[Proveedor]: Proveedor encontrado o None
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
            
    def obtener_componentes_suministrados(self, proveedor_id: int) -> List[Componente]:
        """
        Obtener todos los componentes suministrados por un proveedor
        
        Args:
            proveedor_id (int): ID del proveedor
            
        Returns:
            List[Componente]: Lista de componentes suministrados
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
            
    def buscar_proveedores_por_texto(self, texto: str) -> List[Proveedor]:
        """
        Buscar proveedores por texto en nombre, NIF/CIF o email
        
        Args:
            texto (str): Texto a buscar
            
        Returns:
            List[Proveedor]: Lista de proveedores que coinciden con la búsqueda
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
            
    def _validar_nif_cif(self, nif_cif: str) -> bool:
        """
        Validar formato de NIF/CIF español
        
        Args:
            nif_cif (str): NIF/CIF a validar
            
        Returns:
            bool: True si el formato es válido
        """
        if not nif_cif:
            return False
            
        # Patrón básico para NIF (8 dígitos + letra) o CIF (letra + 7 dígitos + carácter)
        patron_nif = r'^\d{8}[A-Za-z]$'
        patron_cif = r'^[A-Za-z]\d{7}[0-9A-Za-z]$'
        
        return bool(re.match(patron_nif, nif_cif) or re.match(patron_cif, nif_cif))
        
    def _validar_email(self, email: str) -> bool:
        """
        Validar formato de email
        
        Args:
            email (str): Email a validar
            
        Returns:
            bool: True si el formato es válido
        """
        if not email:
            return False
            
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron_email, email))
        
    def actualizar_proveedor(self, proveedor_id: int, **kwargs) -> Optional[Proveedor]:
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
            # Validaciones si se proporcionan estos campos
            if 'nif_cif' in kwargs and kwargs['nif_cif']:
                if not self._validar_nif_cif(kwargs['nif_cif']):
                    raise ValueError(f"El NIF/CIF '{kwargs['nif_cif']}' no tiene un formato válido")
                    
                # Verificar que no exista otro proveedor con el mismo NIF/CIF
                proveedor_existente = self.obtener_por_nif_cif(kwargs['nif_cif'])
                if proveedor_existente and proveedor_existente.id != proveedor_id:
                    raise ValueError(f"Ya existe otro proveedor con NIF/CIF '{kwargs['nif_cif']}'")
                    
            if 'email' in kwargs and kwargs['email']:
                if not self._validar_email(kwargs['email']):
                    raise ValueError(f"El email '{kwargs['email']}' no tiene un formato válido")
                    
            return self.actualizar(proveedor_id, **kwargs)
            
        except ValueError:
            raise
        except SQLAlchemyError as e:
            logger.error(f"❌ Error actualizando proveedor {proveedor_id}: {e}")
            raise
