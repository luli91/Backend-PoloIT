from datetime import datetime
from pydantic import BaseModel
from app.utils.estado_nombre import EstadoNombreEnum
from app.schemas.donacion import DonacionOut
from app.schemas.usuario import UsuarioOut
from typing import Optional

class PublicacionDetalleOut(BaseModel):
    id: int
    mensaje: str
    estado: EstadoNombreEnum
    fecha_publicacion: Optional[datetime]
    imagen_url: Optional[str] = None
    visible: Optional[bool] = None
    donacion: DonacionOut
    usuario: UsuarioOut

    model_config = {"from_attributes": True}