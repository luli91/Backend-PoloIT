from enum import Enum
from pydantic import BaseModel

class EstadoNombre(str, Enum):
    pendiente = "pendiente"
    entregado = "entregado"
    cancelado = "cancelado"

class EstadoBase(BaseModel):
    nombre: EstadoNombre

class EstadoCreate(EstadoBase):
    pass

class EstadoOut(EstadoBase):
    id: int

    class Config:
        from_attributes = True