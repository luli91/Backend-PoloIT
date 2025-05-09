from fastapi import FastAPI
from app.database import Base, engine
from app.models.models import usuario, donacion, categoria, estado, ubicacion
from app.routes import usuarios

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registrar las rutas del módulo usuarios
app.include_router(usuarios.router)

@app.get("/")
def read_root():
    return {"message": "API Donaciones lista"}