from pydantic import BaseModel, EmailStr
from enum import Enum
from .ubicacion import UbicacionOut

# Enum para roles
class RolUsuario(str, Enum):
    usuario = "usuario"
    admin = "admin"

# Para login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Token de acceso
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Para futuros usos como update
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str
    rol: RolUsuario

# El esquema que se usa en POST /usuarios/registro
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str
    password: str
    rol: RolUsuario
    direccion: str
    codigo_postal: str
    ciudad: str
    provincia: str

# Esquema de salida del usuario
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