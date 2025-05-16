from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.estado import Estado
from app.schemas.estado import EstadoCreate, EstadoOut
from app.auth.jwt import solo_admin
from typing import List

router = APIRouter(
    prefix="/estados", 
    tags=["estados"]
)

# Listar todos los estados
@router.get("/", response_model=List[EstadoOut])
def listar_estados(db: Session = Depends(get_db)):
    return db.query(Estado).all()

# Agregar un nuevo estado
@router.post("/", response_model=EstadoOut)
def crear_estado(
    estado: EstadoCreate,
    admin = Depends(solo_admin),
    db: Session = Depends(get_db)
):
    nuevo = Estado(**estado.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# Modificar un estado existente
@router.put("/{estado_id}", response_model=EstadoOut)
def actualizar_estado(
    estado_id: int,
    datos: EstadoCreate,
    admin = Depends(solo_admin),
    db: Session = Depends(get_db)
):
    estado = db.query(Estado).filter(Estado.id == estado_id).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    estado.nombre = datos.nombre
    db.commit()
    db.refresh(estado)
    return estado

# Borrar un estado existente
@router.delete("/{estado_id}")
def eliminar_estado(
    estado_id: int,
    admin = Depends(solo_admin),
    db: Session = Depends(get_db)
):
    estado = db.query(Estado).filter(Estado.id == estado_id).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    db.delete(estado)
    db.commit()
    return {"ok": True, "mensaje": "Estado eliminado"}