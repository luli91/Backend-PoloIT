from pydantic import BaseModel
from typing import Optional
from app.schemas.estado import EstadoOut

class PublicacionCreate(BaseModel):
    mensaje: str
    donacion_id: int

class PublicacionOut(BaseModel):
    id: int
    mensaje: str
    estado: EstadoOut

    model_config = {
        "from_attributes": True
    }