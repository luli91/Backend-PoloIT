from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.database import Base, engine
from app.models import *  # Esto importará todos los modelos definidos en __all__
from app.routers import usuarios, donaciones, publicaciones, categorias, estados, ubicaciones, ping, correos
from app.seed import cargar_categorias, cargar_estados
from fastapi.security import HTTPBearer

load_dotenv()

# Crear tablas (solo si no usamos Alembic)
Base.metadata.create_all(bind=engine)

# Configuración de JWT y seguridad
security = HTTPBearer()

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Donaciones - Polo IT",
    description="""
    # API de Donaciones - Polo IT 🎁

    Esta API permite gestionar donaciones y conectar donantes con beneficiarios.

    ## Características Principales 🌟

    * **Usuarios** 👥
      * Registro y autenticación
      * Roles: usuario y admin
      * Gestión de perfil

    * **Donaciones** 📦
      * Crear y gestionar donaciones
      * Buscar por categoría
      * Seguimiento de estado

    * **Ubicaciones** 📍
      * Búsqueda por ciudad/provincia
      * Filtrado por proximidad

    ## Autenticación 🔐

    Esta API usa JWT (JSON Web Tokens):
    1. Registrarse en `/usuarios/registro`
    2. Obtener token en `/usuarios/login`
    3. Incluir token en header: `Authorization: Bearer <token>`
    """,
    version="1.0.0",
    # Deshabilitar Swagger UI
    docs_url=None,
    # Mantener ReDoc como única documentación
    redoc_url="/",
    contact={
        "name": "Equipo Polo IT",
        "url": "https://github.com/luli91/Backend-PoloIT",
    },
    license_info={
        "name": "MIT",
    },
)


# Personalizar OpenAPI para incluir JWT en la documentación
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Personalizar esquemas de seguridad
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": """
            Para autenticarte:
            1. Usa `/usuarios/login` con email y password
            2. Copia el token JWT recibido
            3. Click en 'Authorize' e ingresa: `Bearer <tu-token>`
            """
        }
    }

    # Aplicar seguridad global
    openapi_schema["security"] = [{"bearerAuth": []}]

    # Personalizar tags
    openapi_schema["tags"] = [
        {
            "name": "usuarios",
            "description": "Gestión de usuarios y autenticación",
            "externalDocs": {
                "description": "Más información",
                "url": "https://github.com/luli91/Backend-PoloIT/wiki/Usuarios"
            }
        },
        {
            "name": "donaciones",
            "description": "Operaciones con donaciones"
        },
        {
            "name": "publicaciones",
            "description": "Gestión de publicaciones de donaciones"
        },
        {
            "name": "categorias",
            "description": "Gestión de categorías de donaciones"
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

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
    allow_origins=["*"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ping)
app.include_router(usuarios)
app.include_router(donaciones)
app.include_router(publicaciones)
app.include_router(categorias)
app.include_router(estados)
app.include_router(ubicaciones)

app.include_router(correos)

# ✅ Endpoint raíz
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API Donaciones lista"}
