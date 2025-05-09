from pydantic import BaseModel, EmailStr
from typing import Optional
from .ubicacion import UbicacionOut

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str
    rol: str
    ubicacion_id: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    telefono: str
    rol: str
    ubicacion: Optional[UbicacionOut]

    class Config:
        orm_mode = True