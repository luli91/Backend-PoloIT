from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from app.database import get_db
from app.models.donacion import Donacion
from app.schemas.donacion import DonacionWithPublicaciones

router = APIRouter()

@router.get("/donaciones/{donacion_id}", response_model=DonacionWithPublicaciones)
def obtener_donacion_completa(donacion_id: int, db: Session = Depends(get_db)):
    donacion = db.query(Donacion)\
        .options(selectinload(Donacion.publicaciones))\
        .filter(Donacion.id == donacion_id).first()
    
    if not donacion:
        raise HTTPException(status_code=404, detail="Donación no encontrada")
    
    return donacion