from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Leer la URL de Supabase desde las variables de entorno (.env)
DATABASE_URL = os.getenv("DATABASE_URL")

# Conectar a la base PostgreSQL usando SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear sesión para usar en las rutas (inyectada con Depends)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase Base que heredan todos los modelos SQLAlchemy
Base = declarative_base()