from pydantic import BaseModel

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaOut(BaseModel):
    id: int
    nombre: str

    model_config = {
        "from_attributes": True
    }