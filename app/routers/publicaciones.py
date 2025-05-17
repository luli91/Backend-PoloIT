from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from typing import List

from app.database import get_db
from app.models.publicacion import Publicacion
from app.models.estado import Estado
from app.schemas.publicacion import PublicacionCreate, PublicacionOut
from app.auth.jwt import obtener_usuario_actual
from app.models.usuario import Usuario

router = APIRouter(
    prefix="/publicaciones",
    tags=["publicaciones"]
)

# Crear una nueva publicación (por default en estado "Activo")
@router.post("/", response_model=PublicacionOut)
def crear_publicacion(
    datos: PublicacionCreate,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    estado = db.query(Estado).filter(Estado.nombre == "Activo").first()
    if not estado:
        raise HTTPException(status_code=500, detail="Estado 'Activo' no encontrado")

    nueva = Publicacion(
        mensaje=datos.mensaje,
        donacion_id=datos.donacion_id,
        usuario_id=usuario_actual.id,
        estado_id=estado.id
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# Obtener todas las publicaciones
@router.get("/", response_model=List[PublicacionOut])
def listar_publicaciones(db: Session = Depends(get_db)):
    return db.query(Publicacion).options(selectinload(Publicacion.estado)).all()

# Obtener una publicación por ID
@router.get("/{publicacion_id}", response_model=PublicacionOut)
def obtener_publicacion(publicacion_id: int, db: Session = Depends(get_db)):
    publicacion = db.query(Publicacion)\
        .options(selectinload(Publicacion.estado))\
        .filter(Publicacion.id == publicacion_id).first()

    if not publicacion:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")

    return publicacion