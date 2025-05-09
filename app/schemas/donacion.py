from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .usuario import UsuarioOut
from .categoria import CategoriaOut
from .estado import EstadoOut

class DonacionBase(BaseModel):
    descripcion: str
    cantidad: float
    imagen_url: Optional[str]
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
        from_attributes = True