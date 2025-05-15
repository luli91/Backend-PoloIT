from pydantic import BaseModel
from datetime import datetime

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

    model_config = {
        "from_attributes": True
    }