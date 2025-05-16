from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from typing import List

from app.database import get_db
from app.models.publicacion import Publicacion
from app.models.donacion import Donacion
from app.models.usuario import Usuario
from app.schemas.publicacion import PublicacionCreate, PublicacionOut, PublicacionUpdate
from app.auth.jwt import obtener_usuario_actual


router = APIRouter(
    prefix="/publicaciones",
    tags=["publicaciones"]
)

# Listar todas las publicaciones visibles
@router.get("/", response_model=list[PublicacionOut])
def listar_publicaciones_visibles(db: Session = Depends(get_db)):
    return db.query(Publicacion)\
        .filter(Publicacion.visible == True)\
        .options(selectinload(Publicacion.estado))\
        .all()

# Listar todas las publicaciones de un usuario
@router.get("/{publicacion_id}", response_model=PublicacionOut)
def obtener_publicacion(publicacion_id: int, db: Session = Depends(get_db)):
    pub = db.query(Publicacion)\
        .options(selectinload(Publicacion.estado))\
        .filter(Publicacion.id == publicacion_id).first()

    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return pub    

# Crear una nueva publicación sobre una donación
@router.post("/", response_model=PublicacionOut)
def crear_publicacion(
    publicacion: PublicacionCreate,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    donacion = db.query(Donacion).filter(Donacion.id == publicacion.donacion_id).first()

    if not donacion:
        raise HTTPException(status_code=404, detail="Donación no encontrada")

    if donacion.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No puedes publicar sobre esta donación")

    nueva_pub = Publicacion(**publicacion.dict())
    db.add(nueva_pub)
    db.commit()
    db.refresh(nueva_pub)
    db.refresh(nueva_pub, attribute_names=["estado"]) #forzar la carga del estado
    return nueva_pub

# Actualizar una publicación
@router.put("/{publicacion_id}", response_model=PublicacionOut)
def actualizar_publicacion(
    publicacion_id: int,
    datos: PublicacionUpdate,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    publicacion = db.query(Publicacion)\
        .options(selectinload(Publicacion.estado), selectinload(Publicacion.donacion))\
        .filter(Publicacion.id == publicacion_id).first()

    if not publicacion:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")

    if publicacion.donacion.usuario_id != usuario_actual.id and usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta publicación")

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(publicacion, campo, valor)

    db.commit()
    db.refresh(publicacion)
    return publicacion

# Mostrar todas las publicaciones de un usuario
@router.get("/mias", response_model=List[PublicacionOut])
def publicaciones_del_usuario(
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    return db.query(Publicacion)\
        .join(Publicacion.donacion)\
        .filter(Donacion.usuario_id == usuario_actual.id)\
        .options(selectinload(Publicacion.estado))\
        .all()