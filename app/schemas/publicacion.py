from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.estado import EstadoOut

class PublicacionBase(BaseModel):
    donacion_id: int
    imagen_url: str
    estado_id: int
    visible: bool = True

class PublicacionCreate(PublicacionBase):
    pass

class PublicacionOut(PublicacionBase):
    id: int
    fecha_publicacion: datetime
    estado: EstadoOut

class PublicacionUpdate(BaseModel):
    imagen_url: Optional[str] = None
    visible: Optional[bool] = None
    estado_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }