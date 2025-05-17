from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.schemas.usuario import UsuarioOut
from app.schemas.categoria import CategoriaOut
from app.schemas.publicacion import PublicacionOut

# Base para creación
class DonacionBase(BaseModel):
    descripcion: str
    cantidad: int
    categoria_id: int

# Para crear una donación
class DonacionCreate(DonacionBase):
    pass

# Respuesta básica con usuario y categoría
class DonacionOut(DonacionBase):
    id: int
    fecha_creacion: datetime
    usuario: UsuarioOut
    categoria: CategoriaOut
    tiene_publicacion: bool

    model_config = {
        "from_attributes": True
    }

# Donación + publicaciones (para detalles)
class DonacionWithPublicaciones(DonacionOut):
    publicaciones: List[PublicacionOut]

    model_config = {
        "from_attributes": True
    }