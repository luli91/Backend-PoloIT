from pydantic import BaseModel
from app.utils.provincias import ProvinciaEnum

class UbicacionBase(BaseModel):
    direccion: str
    ciudad: str
    codigo_postal: str
    provincia: ProvinciaEnum

class UbicacionCreate(UbicacionBase):
    pass

class UbicacionOut(UbicacionBase):
    id: int

    model_config = {
        "from_attributes": True
    }