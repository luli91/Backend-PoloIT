from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
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

# ✅ Middleware para redirigir HTTP a HTTPS
@app.middleware("http")
async def redirect_http_to_https(request: Request, call_next):
    proto = request.headers.get("x-forwarded-proto")
    if proto == "http":
        https_url = request.url.replace(scheme="https")
        return RedirectResponse(url=str(https_url))
    return await call_next(request)

# ✅ Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend-poloitv2-production.up.railway.app",  # Producción
        "http://localhost:5174"  # Desarrollo local
    ],    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Ejecutar seeds al iniciar (solo si las tablas están vacías)
@app.on_event("startup")
def inicializar_datos():
    from app.database import SessionLocal
    print("Ejecutando seeds si hace falta...")
    db = SessionLocal()
    cargar_categorias(db)
    cargar_estados(db)
    db.close()

# ✅ Incluir todos los routers
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
