from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from app.database import get_db
from app.models.donacion import Donacion
from app.schemas.donacion import DonacionCreate, DonacionOut, DonacionWithPublicaciones
from app.models.usuario import Usuario
from app.auth.jwt import obtener_usuario_actual
from app.schemas.paginacion import PaginatedResponse

router = APIRouter(
    prefix="/donaciones",
    tags=["donaciones"]
)

# Listar todas las donaciones
@router.get("/", response_model=PaginatedResponse[DonacionOut])
def listar_donaciones(
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    query = db.query(Donacion).options(
        selectinload(Donacion.usuario),
        selectinload(Donacion.categoria),
        selectinload(Donacion.publicaciones)
    )

    if usuario_actual.rol != "admin":
        query = query.filter(Donacion.usuario_id == usuario_actual.id)

    total = query.count()
    donaciones = query.offset((page - 1) * per_page).limit(per_page).all()

    return PaginatedResponse[DonacionOut](
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page,
        has_next=page * per_page < total,
        has_prev=page > 1,
        items=[DonacionOut.model_validate(d) for d in donaciones]
    )

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
        descripcion=donacion.descripcion,
        cantidad=donacion.cantidad,
        categoria_id=donacion.categoria_id,
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

    donacion.descripcion = datos.descripcion
    donacion.cantidad = datos.cantidad
    donacion.categoria_id = datos.categoria_id

    db.commit()
    db.refresh(donacion)

    # ❌ Esta línea se elimina: donacion.tiene_publicacion = ...
    return donacion

# Eliminar una donación propia
@router.delete("/{donacion_id}")
def eliminar_donacion(
    donacion_id: int,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    donacion = db.query(Donacion)\
        .options(selectinload(Donacion.publicaciones))\
        .filter(Donacion.id == donacion_id).first()

    if not donacion:
        raise HTTPException(status_code=404, detail="Donación no encontrada")

    if donacion.usuario_id != usuario_actual.id and usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta donación")

    if len(donacion.publicaciones) > 0:
        raise HTTPException(status_code=400, detail="No se puede eliminar una donación que ya tiene publicación")

    db.delete(donacion)
    db.commit()
    return {"ok": True, "mensaje": "Donación eliminada"}
