from pydantic import BaseModel
from datetime import datetime
from typing import List
from schemas.publicacion import PublicacionOut

class DonacionBase(BaseModel):
    descripcion: str
    cantidad: int
    usuario_id: int
    categoria_id: int

class DonacionCreate(DonacionBase):
    pass

class DonacionOut(DonacionBase):
    id: int
    fecha_creacion: datetime

    model_config = {
        "from_attributes": True
    }
    
class DonacionWithPublicaciones(DonacionOut):
    publicaciones: List[PublicacionOut]

    model_config = {
        "from_attributes": True
    }