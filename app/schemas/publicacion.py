from pydantic import BaseModel
from typing import Optional
from app.utils.estado_nombre import EstadoNombreEnum

# Crear publicaciones nuevas
class PublicacionCreate(BaseModel):
    mensaje: str
    donacion_id: int

# Respuesta limpia y tipada para visualizar publicaciones
class PublicacionOut(BaseModel):
    id: int
    mensaje: str
    estado: EstadoNombreEnum

    model_config = {
        "from_attributes": True
    }

# Cambiar unicamente el estado
class PublicacionEstadoUpdate(BaseModel):
    estado: EstadoNombreEnum

# Actualizar parcialmente cualquier campo, útil para editar desde una donación
class PublicacionUpdate(BaseModel):
    mensaje: Optional[str] = None
    estado: Optional[EstadoNombreEnum] = None
    imagen_url: Optional[str] = None
    visible: Optional[bool] = None