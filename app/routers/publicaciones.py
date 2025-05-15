
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.publicacion import Publicacion
from app.schemas.publicacion import PublicacionCreate, PublicacionOut

router = APIRouter(
    prefix="/publicaciones",
    tags=["publicaciones"]
)

@router.post("/", response_model=PublicacionOut)
def crear_publicacion(publicacion: PublicacionCreate, db: Session = Depends(get_db)):
    nueva_pub = Publicacion(**publicacion.dict())
    db.add(nueva_pub)
    db.commit()
    db.refresh(nueva_pub)
    return nueva_pub

@router.get("/", response_model=list[PublicacionOut])
def listar_publicaciones(db: Session = Depends(get_db)):
    return db.query(Publicacion).all()

@router.get("/{publicacion_id}", response_model=PublicacionOut)
def obtener_publicacion(publicacion_id: int, db: Session = Depends(get_db)):
    pub = db.query(Publicacion).filter(Publicacion.id == publicacion_id).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return pub