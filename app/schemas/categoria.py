from pydantic import BaseModel

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaOut(CategoriaBase):
    id: int

    model_config = {
        "from_attributes": True
    }