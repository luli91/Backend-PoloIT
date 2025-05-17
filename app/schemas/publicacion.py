from pydantic import BaseModel
from typing import Optional
from app.utils.estado_nombre import EstadoNombreEnum

class PublicacionCreate(BaseModel):
    mensaje: str
    donacion_id: int

class PublicacionOut(BaseModel):
    id: int
    mensaje: str
    estado: EstadoNombreEnum
    
    model_config = {
        "from_attributes": True
    }

class PublicacionEstadoUpdate(BaseModel):
    estado: EstadoNombreEnum