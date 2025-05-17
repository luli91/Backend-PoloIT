from pydantic import BaseModel
from app.utils.estado_nombre import EstadoNombreEnum

class EstadoBase(BaseModel):
    nombre: EstadoNombreEnum

class EstadoCreate(EstadoBase):
    pass

class EstadoOut(EstadoBase):
    id: int

    model_config = {
        "from_attributes": True
    }