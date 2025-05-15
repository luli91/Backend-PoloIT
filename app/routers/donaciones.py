from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from typing import List

from app.database import get_db
from app.models.donacion import Donacion
from app.schemas.donacion import DonacionCreate, DonacionOut, DonacionWithPublicaciones
from app.models.usuario import Usuario
from app.auth.jwt import obtener_usuario_actual, solo_admin

router = APIRouter(
    prefix="/donaciones",
    tags=["donaciones"]
)

# Listar todas las donaciones
@router.get("/", response_model=List[DonacionOut])
def listar_donaciones(db: Session = Depends(get_db)):
    return db.query(Donacion)\
        .options(
            selectinload(Donacion.usuario),
            selectinload(Donacion.categoria)
        ).all()

# Ver detalles de una donación
@router.get("/{donacion_id}", response_model=DonacionWithPublicaciones)
def obtener_donacion_completa(donacion_id: int, db: Session = Depends(get_db)):
    donacion = db.query(Donacion)\
        .options(
            selectinload(Donacion.publicaciones),
            selectinload(Donacion.usuario),
            selectinload(Donacion.categoria)
        )\
        .filter(Donacion.id == donacion_id).first()

    if not donacion:
        raise HTTPException(status_code=404, detail="Donación no encontrada")

    return donacion

# Crear una nueva donación
@router.post("/", response_model=DonacionOut, status_code=status.HTTP_201_CREATED)
def crear_donacion(
    donacion: DonacionCreate,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    nueva_donacion = Donacion(
        **donacion.dict(),
        usuario_id=usuario_actual.id
    )
    db.add(nueva_donacion)
    db.commit()
    db.refresh(nueva_donacion)
    return nueva_donacion

# Actualizar una donación propia
@router.put("/{donacion_id}", response_model=DonacionOut)
def actualizar_donacion(
    donacion_id: int,
    datos: DonacionCreate,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    donacion = db.query(Donacion).filter(Donacion.id == donacion_id).first()

    if not donacion:
        raise HTTPException(status_code=404, detail="Donación no encontrada")

    if donacion.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta donación")

    for campo, valor in datos.dict().items():
        setattr(donacion, campo, valor)

    db.commit()
    db.refresh(donacion)
    return donacion

# Eliminar una donación propia
@router.delete("/{donacion_id}")
def eliminar_donacion(
    donacion_id: int,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    donacion = db.query(Donacion).filter(Donacion.id == donacion_id).first()

    if not donacion:
        raise HTTPException(status_code=404, detail="Donación no encontrada")

    if donacion.usuario_id != usuario_actual.id and usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta donación")

    db.delete(donacion)
    db.commit()
    return {"ok": True, "mensaje": "Donación eliminada"}