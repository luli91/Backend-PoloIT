from fastapi import FastAPI
from database import Base, engine
from models import *

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API Donaciones lista"}