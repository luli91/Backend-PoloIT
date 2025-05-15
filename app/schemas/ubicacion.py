from pydantic import BaseModel

class UbicacionBase(BaseModel):
    direccion: str
    codigo_postal: str
    ciudad: str
    provincia: str

class UbicacionCreate(UbicacionBase):
    pass

class UbicacionOut(UbicacionBase):
    id: int

    model_config = {
        "from_attributes": True
    }