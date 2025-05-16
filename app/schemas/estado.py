from enum import Enum
from pydantic import BaseModel

class EstadoNombre(str, Enum):
    pendiente = "Pendiente"
    entregado = "Entregado"
    cancelado = "Cancelado"

class EstadoBase(BaseModel):
    nombre: EstadoNombre

class EstadoCreate(EstadoBase):
    pass

class EstadoOut(EstadoBase):
    id: int

    model_config = {
        "from_attributes": True
    }