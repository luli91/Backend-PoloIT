from pydantic import BaseModel
from app.utils.estado_nombre import EstadoNombreEnum
from app.schemas.donacion import DonacionOut
from app.schemas.usuario import UsuarioOut

class PublicacionDetalleOut(BaseModel):
    id: int
    mensaje: str
    estado: EstadoNombreEnum
    donacion: DonacionOut
    usuario: UsuarioOut

    model_config = {"from_attributes": True}
