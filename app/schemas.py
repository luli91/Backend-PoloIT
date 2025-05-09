from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# -------- UBICACION --------

class UbicacionBase(BaseModel):
    direccion: str
    codigo_postal: str
    ciudad: str
    provincia: str

class UbicacionCreate(UbicacionBase):
    pass

class UbicacionOut(UbicacionBase):
    id: int

    class Config:
        orm_mode = True


# -------- USUARIO --------

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
    ubicacion: Optional[UbicacionOut] = None

    class Config:
        orm_mode = True


# -------- CATEGORIA --------

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaOut(CategoriaBase):
    id: int

    class Config:
        orm_mode = True


# -------- ESTADO --------

class EstadoBase(BaseModel):
    nombre: str

class EstadoCreate(EstadoBase):
    pass

class EstadoOut(EstadoBase):
    id: int

    class Config:
        orm_mode = True


# -------- DONACION --------

class DonacionBase(BaseModel):
    descripcion: str
    cantidad: float
    imagen_url: Optional[str] = None
    usuario_id: int
    categoria_id: int
    estado_id: int

class DonacionCreate(DonacionBase):
    pass

class DonacionOut(DonacionBase):
    id: int
    fecha_creacion: datetime
    usuario: UsuarioOut
    categoria: CategoriaOut
    estado: EstadoOut

    class Config:
        orm_mode = True