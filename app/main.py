from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import usuario, donacion, categoria, estado, ubicacion, publicacion
from app.routers import usuarios, donaciones, publicaciones, categorias, estados, ubicaciones, ping

# Crear tablas en la base de datos (porque no uso Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Donaciones",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos los routers
app.include_router(ping)
app.include_router(usuarios)
app.include_router(donaciones)
app.include_router(publicaciones)
app.include_router(categorias)
app.include_router(estados)
app.include_router(ubicaciones)

# Endpoint raíz
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API Donaciones lista"}