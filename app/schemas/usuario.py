from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from .ubicacion import UbicacionOut

class RolUsuario(str, Enum):
    usuario = "usuario"
    admin = "admin"
# NOTA: Actualmente los roles están limitados a "usuario" y "admin" por simplicidad.

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str
    rol: RolUsuario
    ubicacion_id: int

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    telefono: str
    rol: str
    ubicacion: UbicacionOut

    model_config = {
        "from_attributes": True
    }