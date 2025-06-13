from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import usuario, donacion, categoria, estado, ubicacion, publicacion
from app.routers import usuarios, donaciones, publicaciones, categorias, estados, ubicaciones, ping
from app.seed import cargar_categorias, cargar_estados

# Crear tablas (solo si no usamos Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Donaciones",
    version="0.1.0"
)

# Ejecutar seeds al iniciar (solo si las tablas están vacías)
@app.on_event("startup")
def inicializar_datos():
    from app.database import SessionLocal
    print("Ejecutando seeds si hace falta...")
    db = SessionLocal()
    cargar_categorias(db)
    cargar_estados(db)
    db.close()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar esto en producción
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

# ✅ Endpoint raíz
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API Donaciones lista"}
