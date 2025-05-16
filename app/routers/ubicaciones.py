from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.ubicacion import Ubicacion
from app.models.usuario import Usuario
from app.schemas.ubicacion import UbicacionCreate, UbicacionOut
from app.auth.jwt import obtener_usuario_actual

router = APIRouter(
    prefix="/ubicaciones",
    tags=["ubicaciones"]
)

# Encontrar donaciones cercanas
@router.get("/", response_model=List[UbicacionOut])
def buscar_ubicaciones(
    ciudad: Optional[str] = None,
    provincia: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Ubicacion)
    
    if ciudad:
        query = query.filter(Ubicacion.ciudad.ilike(f"%{ciudad}%"))
    if provincia:
        query = query.filter(Ubicacion.provincia.ilike(f"%{provincia}%"))

    return query.all()

# Obtener ubicación del usuario actual
@router.get("/mia", response_model=UbicacionOut)
def obtener_mi_ubicacion(
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    if not usuario.ubicacion_id:
        raise HTTPException(status_code=404, detail="El usuario no tiene ubicación asignada")

    ubicacion = db.query(Ubicacion).filter(Ubicacion.id == usuario.ubicacion_id).first()
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    
    return ubicacion

# Crear ubicación (si el usuario aún no tiene una)
@router.post("/", response_model=UbicacionOut)
def crear_ubicacion(
    ubicacion: UbicacionCreate,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    if usuario.ubicacion_id:
        raise HTTPException(status_code=400, detail="El usuario ya tiene una ubicación")

    nueva = Ubicacion(**ubicacion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    # Asociar ubicación al usuario
    usuario.ubicacion_id = nueva.id
    db.commit()

    return nueva

# Editar solo si pertenece al usuario
@router.put("/{ubicacion_id}", response_model=UbicacionOut)
def actualizar_ubicacion(
    ubicacion_id: int,
    datos: UbicacionCreate,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    if usuario.ubicacion_id != ubicacion_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta ubicación")

    ubicacion = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    for campo, valor in datos.dict().items():
        setattr(ubicacion, campo, valor)

    db.commit()
    db.refresh(ubicacion)
    return ubicacion