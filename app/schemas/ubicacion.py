from pydantic import BaseModel
from app.utils.provincias import ProvinciaEnum

class UbicacionBase(BaseModel):
    provincia: ProvinciaEnum
    ciudad: str
    direccion: str
    codigo_postal: str

class UbicacionCreate(UbicacionBase):
    pass

class UbicacionOut(UbicacionBase):
    id: int

    model_config = {
        "from_attributes": True
    }