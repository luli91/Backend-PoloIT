from pydantic import BaseModel
from datetime import datetime
from typing import List

from app.schemas.usuario import UsuarioOut
from app.schemas.categoria import CategoriaOut
from app.schemas.publicacion import PublicacionOut

# Base para creación
class DonacionBase(BaseModel):
    descripcion: str
    cantidad: int
    categoria_id: int
    estado_id: int 

# Para crear una donación
class DonacionCreate(DonacionBase):
    pass

# Respuesta básica con usuario y categoría
class DonacionOut(DonacionBase):
    id: int
    fecha_creacion: datetime
    usuario: UsuarioOut
    categoria: CategoriaOut

    model_config = {
        "from_attributes": True
    }

# Respuesta extendida con publicaciones
class DonacionWithPublicaciones(DonacionOut):
    publicaciones: List[PublicacionOut]

    model_config = {
        "from_attributes": True
    }