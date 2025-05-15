from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import usuario, donacion, categoria, estado, ubicacion
from app.routes import usuarios, ping

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Donaciones", version="0.1.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #TBD reemplazar por dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(usuarios.router)
app.include_router(ping.router) 

# Endpoint raíz opcional
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API Donaciones lista"}