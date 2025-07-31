from re import match
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class ProveedorBase(BaseModel):
    nombre: str = Field(..., description="Nombre del proveedor")
    nif_cif: Optional[str] = Field(None, description="NIF/CIF del proveedor")
    direccion: Optional[str] = Field(None, description="Dirección del proveedor")
    telefono: Optional[str] = Field(None, description="Teléfono del proveedor")
    email: Optional[EmailStr] = Field(None, description="Email del proveedor")
    activo: bool = Field(True, description="Estado del proveedor")
    @field_validator('nombre')
    def nombre_vacion(cls, v):
        if len(v.strip()) < 1:
            raise ValueError("El nombre del proveedor no puede estar vacío")
        return v.strip()
    @field_validator('email')
    def email_valido(cls, v):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if v and not match(pattern, v):
            raise ValueError("El email debe ser una dirección de correo electrónico válida")
    @field_validator('telefono')
    def telefono_valido(cls, v):
        # Permitir números, espacios, guiones y paréntesis, opcionalmente con prefijo internacional
        pattern = r"^\+?[\d\s\-\(\)]{9,}$"
        if v and not match(pattern, v):
            raise ValueError("Teléfono inválido")
        return v
    

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, description="Nombre del proveedor")
    nif_cif: Optional[str] = Field(None, description="NIF/CIF del proveedor")
    direccion: Optional[str] = Field(None, description="Dirección del proveedor")
    telefono: Optional[str] = Field(None, description="Teléfono del proveedor")
    email: Optional[EmailStr] = Field(None, description="Email del proveedor")
    activo: Optional[bool] = Field(None, description="Estado del proveedor")
    @field_validator('nombre')
    def nombre_vacion(cls, v):
        if len(v.strip()) < 1:
            raise ValueError("El nombre del proveedor no puede estar vacío")
        return v.strip()
    @field_validator('email')
    def email_valido(cls, v):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if v and not match(pattern, v):
            raise ValueError("El email debe ser una dirección de correo electrónico válida")
    @field_validator('telefono')
    def telefono_valido(cls, v):
        # Permitir números, espacios, guiones y paréntesis, opcionalmente con prefijo internacional
        pattern = r"^\+?[\d\s\-\(\)]{9,}$"
        if v and not match(pattern, v):
            raise ValueError("Teléfono inválido")
        return v

class ProveedorInDB(ProveedorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

class ProveedorResponse(ProveedorInDB):
    pass
