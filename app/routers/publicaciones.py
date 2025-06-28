from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from typing import List

from app.database import get_db
from app.models.publicacion import Publicacion
from app.models.estado import Estado
from app.models.donacion import Donacion
from app.schemas.paginacion import PaginatedResponse
from app.schemas.publicacion import PublicacionCreate, PublicacionOut, PublicacionEstadoUpdate, PublicacionUpdate
from app.auth.jwt import obtener_usuario_actual
from app.schemas.publicacion_detalle import PublicacionDetalleOut
from app.models.usuario import Usuario

router = APIRouter(
    prefix="/publicaciones",
    tags=["publicaciones"]
)

# Crear una nueva publicación (una por donación y por default en estado "Activo")
@router.post("/", response_model=PublicacionOut)
def crear_publicacion(
    datos: PublicacionCreate,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    donacion = db.query(Donacion).filter(
        Donacion.id == datos.donacion_id,
        Donacion.usuario_id == usuario_actual.id
    ).first()
    if not donacion:
        raise HTTPException(status_code=404, detail="Donación no encontrada o no es tuya")

    existente = db.query(Publicacion).filter(Publicacion.donacion_id == datos.donacion_id).first()
    if existente:
        raise HTTPException(status_code=400, detail="Esta donación ya tiene una publicación. Podés editarla.")

    estado = db.query(Estado).filter(Estado.nombre == "Pendiente").first()
    if not estado:
        raise HTTPException(status_code=500, detail="Estado 'Pendiente' no encontrado")

    nueva = Publicacion(
        mensaje=datos.mensaje,
        donacion_id=datos.donacion_id,
        usuario_id=usuario_actual.id,
        estado_id=estado.id
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return PublicacionOut.model_validate(nueva)


# Listar todas las publicaciones
@router.get("/", response_model=List[PublicacionOut])
def listar_publicaciones(db: Session = Depends(get_db)):
    publicaciones = db.query(Publicacion).options(selectinload(Publicacion.estado)).all()
    return [PublicacionOut.model_validate(p) for p in publicaciones]


# Obtener publicaciones con detalles:

from app.schemas.publicacion_detalle import PublicacionDetalleOut

@router.get("/detalle", response_model=PaginatedResponse[PublicacionDetalleOut])
def publicaciones_con_paginacion(
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Publicacion).options(
        selectinload(Publicacion.estado),
        selectinload(Publicacion.donacion).selectinload(Donacion.categoria),
        selectinload(Publicacion.usuario).selectinload(Usuario.ubicacion)
    )

    total = query.count()
    publicaciones = query.offset((page - 1) * per_page).limit(per_page).all()

    return PaginatedResponse[PublicacionDetalleOut](
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page,
        has_next=page * per_page < total,
        has_prev=page > 1,
        items=[PublicacionDetalleOut.model_validate(p) for p in publicaciones]
    )

# Obtener mis publicaciones:

@router.get("/mis", response_model=PaginatedResponse[PublicacionDetalleOut])
def mis_publicaciones_paginadas(
    page: int = 1,
    per_page: int = 10,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    query = db.query(Publicacion).filter(
        Publicacion.usuario_id == usuario_actual.id
    ).options(
        selectinload(Publicacion.estado),
        selectinload(Publicacion.donacion).selectinload(Donacion.categoria),
        selectinload(Publicacion.usuario).selectinload(Usuario.ubicacion)
    )

    total = query.count()
    publicaciones = query.offset((page - 1) * per_page).limit(per_page).all()

    return PaginatedResponse[PublicacionDetalleOut](
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page,
        has_next=page * per_page < total,
        has_prev=page > 1,
        items=[PublicacionDetalleOut.model_validate(p) for p in publicaciones]
    )

# Obtener una publicación por ID
@router.get("/{publicacion_id}", response_model=PublicacionOut)
def obtener_publicacion(publicacion_id: int, db: Session = Depends(get_db)):
    publicacion = db.query(Publicacion)\
        .options(selectinload(Publicacion.estado))\
        .filter(Publicacion.id == publicacion_id).first()

    if not publicacion:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")

    return PublicacionOut.model_validate(publicacion)


# Obtener una publicación por donación (1:1)
@router.get("/por-donacion/{donacion_id}", response_model=PublicacionOut)
def obtener_por_donacion(
    donacion_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    publicacion = db.query(Publicacion).filter(
        Publicacion.donacion_id == donacion_id
    ).first()
    if not publicacion:
        raise HTTPException(status_code=404, detail="No hay publicación para esta donación")
    return PublicacionOut.model_validate(publicacion)

# Cambiar el estado de una publicación (solo propio o admin)
@router.put("/{publicacion_id}/estado", response_model=PublicacionOut)
def cambiar_estado_publicacion(
    publicacion_id: int,
    datos: PublicacionEstadoUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    publicacion = db.query(Publicacion).filter(Publicacion.id == publicacion_id).first()
    if not publicacion:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")

    if publicacion.usuario_id != usuario_actual.id and usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    nuevo_estado = db.query(Estado).filter(Estado.nombre == datos.estado).first()
    if not nuevo_estado:
        raise HTTPException(status_code=400, detail="Estado no válido")

    publicacion.estado_id = nuevo_estado.id
    db.commit()
    db.refresh(publicacion)
    return PublicacionOut.model_validate(publicacion)

# Actualizar publicación por donación (si ya existe)
# @router.put("/por-donacion/{donacion_id}", response_model=PublicacionOut)
# def actualizar_publicacion_por_donacion(
#     donacion_id: int,
#     datos: PublicacionUpdate,
#     db: Session = Depends(get_db),
#     usuario_actual: Usuario = Depends(obtener_usuario_actual)
# ):
#     donacion = db.query(Donacion).filter(
#         Donacion.id == donacion_id,
#         Donacion.usuario_id == usuario_actual.id
#     ).first()
#     if not donacion:
#         raise HTTPException(status_code=403, detail="No tenés permiso para esta donación")
#
#     publicacion = db.query(Publicacion).filter(
#         Publicacion.donacion_id == donacion_id
#     ).first()
#
#     if not publicacion:
#         raise HTTPException(status_code=404, detail="No hay publicación para esta donación")
#
#     for campo, valor in datos.dict(exclude_unset=True).items():
#         setattr(publicacion, campo, valor)
#
#     db.commit()
#     db.refresh(publicacion)
#     return PublicacionOut.model_validate(publicacion)
@router.put("/por-donacion/{donacion_id}", response_model=PublicacionOut)
def actualizar_publicacion_por_donacion(
    donacion_id: int,
    datos: PublicacionUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    donacion = db.query(Donacion).filter(
        Donacion.id == donacion_id,
        Donacion.usuario_id == usuario_actual.id
    ).first()
    if not donacion:
        raise HTTPException(status_code=403, detail="No tenés permiso para esta donación")

    publicacion = db.query(Publicacion).filter(
        Publicacion.donacion_id == donacion_id
    ).first()

    if not publicacion:
        raise HTTPException(status_code=404, detail="No hay publicación para esta donación")

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(publicacion, campo, valor)

    db.commit()
    db.refresh(publicacion)
    return PublicacionOut.model_validate(publicacion)

# Eliminar una publicacion
@router.delete("/{publicacion_id}")
def eliminar_publicacion(
    publicacion_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    publicacion = db.query(Publicacion).filter(Publicacion.id == publicacion_id).first()

    if not publicacion:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")

    if publicacion.usuario_id != usuario_actual.id and usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta publicación")

    db.delete(publicacion)
    db.commit()

    return {"ok": True, "mensaje": "Publicación eliminada"}

