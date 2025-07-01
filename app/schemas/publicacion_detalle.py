from datetime import datetime
from pydantic import BaseModel
from app.utils.estado_nombre import EstadoNombreEnum
from app.schemas.donacion import DonacionOut
from typing import Optional

class PublicacionDetalleOut(BaseModel):
    id: int
    mensaje: str
    estado_nombre: EstadoNombreEnum
    fecha_publicacion: Optional[datetime]
    imagen_url: Optional[str] = None
    visible: Optional[bool] = None
    donacion: DonacionOut

    model_config = {"from_attributes": True}

