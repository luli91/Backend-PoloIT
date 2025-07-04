# 🧾 Backend Polo IT – Proyecto de Donaciones

Este proyecto es el backend de una plataforma de donaciones desarrollada como parte del programa Polo IT.
Permite a personas registrarse, ofrecer donaciones (objetos o servicios) y gestionar su disponibilidad mediante publicaciones.
El backend fue construido con `FastAPI`, con persistencia en `PostgreSQL` (vía `Supabase`) y autenticación basada en `JWT`.

✨ Funcionalidades principales
- Registro, login y perfil de usuarios con control de acceso (`usuario`, `admin`)
- Gestión de donaciones (crear, editar, eliminar, listar)
- Publicaciones con visibilidad controlada y estado (`Pendiente`, `Entregado`, `Cancelado`)
- Ubicaciones personales para búsqueda local por ciudad/provincia
- Seeds automáticos para datos base (para categorías y estados)
- Estructura modular y lista para integrar frontend o deploy

💡 PRÓXIMAMENTE: integración con Cloudinary para subir imágenes de las publicaciones.

---

## ⚙️ Tecnologías utilizadas
- [FastAPI](https://fastapi.tiangolo.com/) – Framework principal para la API
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM para modelado de datos
- [Pydantic v2](https://docs.pydantic.dev/latest/) – Validación de datos y serialización
- [PostgreSQL (via Supabase)](https://supabase.com/) – Base de datos remota
- [Uvicorn](https://www.uvicorn.org/) – Servidor ASGI para desarrollo
- [Cloudinary](https://cloudinary.com/) – Almacenamiento de imágenes (**INTEGRACIÓN PENDIENTE**)
- Autenticación JWT implementada con `OAuth2PasswordBearer` (solo para extracción de token) 
- Uso de tokens y control de acceso por rol (`usuario`, `admin`)

---

## 🗂️ Estructura del proyecto

```plaintext
Backend-PoloIT/
├── app/
│   ├── main.py                     # Punto de entrada de la app, configuración de routers y CORS
│   ├── database.py                 # Conexión a Supabase/PostgreSQL (SQLAlchemy)
│   ├── cloudinary_config.py        # Configuración para subir imágenes (PENDIENTE)
│   ├── seed.py                     # Carga automática de categorías y estados iniciales
│
│   ├── models/                     # Modelos SQLAlchemy (tablas de la base de datos)
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── donacion.py
│   │   ├── categoria.py
│   │   ├── estado.py
│   │   ├── ubicacion.py
│   │   └── publicacion.py
│
│   ├── schemas/                    # Esquemas Pydantic para validación y respuestas
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── donacion.py
│   │   ├── categoria.py
│   │   ├── estado.py
│   │   ├── ubicacion.py
│   │   └── publicacion.py
│
│   ├── routers/                    # Rutas de la API REST organizadas por entidad
│   │   ├── __init__.py
│   │   ├── usuarios.py             # Registro, login, perfil, gestión admin
│   │   ├── donaciones.py           # CRUD de donaciones
│   │   ├── publicaciones.py        # Crear, listar, editar publicaciones
│   │   ├── categorias.py           # Listar y administrar categorías (admin)
│   │   ├── estados.py              # Listar y administrar estados (admin)
│   │   ├── ubicaciones.py          # Gestión de ubicación personal y filtros
│   │   └── ping.py                 # Health check simple
│
│   ├── auth/                       # Autenticación y autorización
│   │   ├── __init__.py
│   │   ├── hashing.py              # Hasheo y verificación de contraseñas
│   │   └── jwt.py                  # Generación y validación de tokens JWT
│
├── .env.example                    # Plantilla para configurar variables de entorno
├── requirements.txt                # Librerías necesarias para el entorno
├── README.md                       # Documentación del proyecto
```
---

## 🚀 Cómo correr el proyecto localmente

### 1. Clonar el repositorio
```bash
git clone https://github.com/luli91/Backend-PoloIT.git
cd Backend-PoloIT
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crear un archivo `.env` basado en `.env.example`
```bash
cp .env.example .env
```
Editar `.env` con las credenciales de base de datos, JWT secret y (PROXIMAMENTE) Cloudinary.

Y completar los valores reales de:
- DATABASE_URL
- JWT_SECRET
- CLOUDINARY_* (PENDIENTE)

### 4. Ejecutar el servidor
```bash
uvicorn main:app --reload
```


El backend estará disponible en:
📍 http://127.0.0.1:8000

Documentación automática:
📘 http://127.0.0.1:8000/docs
🔧 http://127.0.0.1:8000/redoc (alternativa)

La carga de datos iniciales (categorías y estados) se hace automáticamente al iniciar, por `@app.on_event("startup")`.

---

## 🔍 Health Check

`GET /ping`  
Devuelve `{"message": "pong"}`  
Sirve para verificar que la API esté corriendo correctamente.

---

## 💻 Cómo contribuir

- Cloná el proyecto
- Creá una nueva rama: `git checkout -b nombre-tarea`
- Hacé tus cambios y commit: `git commit -m "Detalle del cambio realizado"`
- Subí la rama: `git push origin nombre-tarea`
- Hacé un Pull Request en GitHub