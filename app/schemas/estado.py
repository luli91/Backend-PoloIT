from pydantic import BaseModel

class EstadoBase(BaseModel):
    nombre: str

class EstadoCreate(EstadoBase):
    pass

class EstadoOut(EstadoBase):
    id: int

    class Config:
        from_attributes = True