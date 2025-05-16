from pydantic import BaseModel
from datetime import datetime
from typing import List

from app.schemas.usuario import UsuarioOut
from app.schemas.categoria import CategoriaOut
from app.schemas.publicacion import PublicacionOut

# Base para creacion
class DonacionBase(BaseModel):
    descripcion: str
    cantidad: int
    categoria_id: int

# Para crear
class DonacionCreate(DonacionBase):
    pass

# Respuesta básica con relaciones cargadas
class DonacionOut(DonacionBase):
    id: int
    fecha_creacion: datetime
    usuario: UsuarioOut
    categoria: CategoriaOut

    model_config = {
        "from_attributes": True
    }

# Para incluir publicaciones   
class DonacionWithPublicaciones(DonacionOut):
    publicaciones: List[PublicacionOut]

    model_config = {
        "from_attributes": True
    }