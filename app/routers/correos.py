from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.servicio_correo import ServicioCorreo
from app.models import Donacion, Usuario, Publicacion, RegistroCorreo
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

router = APIRouter(
    prefix="/notificaciones",
    tags=["notificaciones"]
)

servicio_correo = ServicioCorreo()


class SolicitudNotificacionCorreo(BaseModel):
    donacion_id: int


class RespuestaRegistroCorreo(BaseModel):
    id: int
    donacion_id: int
    destinatario: str
    estado: str
    id_mensaje: Optional[str]
    fecha_envio: datetime
    detalles_error: Optional[str]


@router.post(
    "/donacion",
    summary="Envía notificación por correo de una donación",
    description="Envía un correo electrónico al receptor de una donación con los detalles de la misma",
    response_description="Confirmación del envío del correo"
)
async def enviar_notificacion_donacion(
    solicitud: SolicitudNotificacionCorreo,
    db: Session = Depends(get_db)
):
    # Obtener la donación y sus relaciones
    donacion = db.query(Donacion).filter(Donacion.id == solicitud.donacion_id).first()
    if not donacion:
        raise HTTPException(status_code=404, detail="Donación no encontrada")

    # Obtener la publicación asociada
    publicacion = db.query(Publicacion).filter(
        Publicacion.donacion_id == donacion.id
    ).first()
    if not publicacion:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")

    # Obtener usuarios involucrados
    donante = db.query(Usuario).filter(Usuario.id == donacion.usuario_id).first()
    receptor = db.query(Usuario).filter(Usuario.id == publicacion.usuario_id).first()

    # Preparar datos para el correo
    datos_correo = {
        "nombre_remitente": donante.nombre,
        "correo_remitente": donante.email,
        "nombre_destinatario": receptor.nombre,
        "correo_destinatario": receptor.email,
        "categoria": donacion.categoria.nombre,
        "cantidad": donacion.cantidad,
        "descripcion": donacion.descripcion,
        "mensaje_publicacion": publicacion.mensaje,
        "donacion_id": donacion.id
    }

    # ✅ Llamada asincrónica al servicio de correo
    return await servicio_correo.enviar_notificacion_donacion(datos_correo, db)


@router.get(
    "/registros/{donacion_id}",
    response_model=List[RespuestaRegistroCorreo],
    summary="Obtiene los registros de correos enviados para una donación",
    description="Retorna el historial de envíos de correos para una donación específica"
)
async def obtener_registros_correo(
    donacion_id: int,
    db: Session = Depends(get_db)
):
    registros = db.query(RegistroCorreo).filter(
        RegistroCorreo.donacion_id == donacion_id
    ).all()

    if not registros:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron registros de correos para esta donación"
        )

    return registros
