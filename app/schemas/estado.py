from pydantic import BaseModel
from app.models.estado import EstadoNombreEnum

# Enum importado del modelo
class EstadoBase(BaseModel):
    nombre: EstadoNombreEnum

class EstadoCreate(EstadoBase):
    pass

class EstadoOut(EstadoBase):
    id: int

    model_config = {
        "from_attributes": True
    }