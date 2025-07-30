from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class ProveedorBase(BaseModel):
    nombre: str = Field(..., description="Nombre del proveedor")
    ruc: Optional[str] = Field(None, description="RUC del proveedor")
    direccion: Optional[str] = Field(None, description="Dirección del proveedor")
    telefono: Optional[str] = Field(None, description="Teléfono del proveedor")
    email: Optional[EmailStr] = Field(None, description="Email del proveedor")
    contacto: Optional[str] = Field(None, description="Persona de contacto")
    activo: bool = Field(True, description="Estado del proveedor")

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, description="Nombre del proveedor")
    ruc: Optional[str] = Field(None, description="RUC del proveedor")
    direccion: Optional[str] = Field(None, description="Dirección del proveedor")
    telefono: Optional[str] = Field(None, description="Teléfono del proveedor")
    email: Optional[EmailStr] = Field(None, description="Email del proveedor")
    contacto: Optional[str] = Field(None, description="Persona de contacto")
    activo: Optional[bool] = Field(None, description="Estado del proveedor")

class ProveedorInDB(ProveedorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ProveedorResponse(ProveedorInDB):
    pass
