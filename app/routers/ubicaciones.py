from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ubicacion import Ubicacion
from app.schemas.ubicacion import UbicacionCreate, UbicacionOut
from typing import List

router = APIRouter(prefix="/ubicaciones", tags=["ubicaciones"])

@router.get("/", response_model=List[UbicacionOut])
def listar_ubicaciones(db: Session = Depends(get_db)):
    return db.query(Ubicacion).all()

@router.post("/", response_model=UbicacionOut)
def crear_ubicacion(ubicacion: UbicacionCreate, db: Session = Depends(get_db)):
    nueva = Ubicacion(**ubicacion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva