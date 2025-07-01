import httpx
import os
from typing import Dict
from datetime import datetime
import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.registro_correo import RegistroCorreo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServicioCorreo:
    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY")
        self.correo_remitente = os.getenv("SENDGRID_FROM_EMAIL")

    async def enviar_notificacion_donacion(self, datos_donacion: Dict, db: Session) -> Dict:
        self._validar_datos_correo(datos_donacion)

        contenido_html = f"""
        <html>
            <body>
                <h2>¡Hola {datos_donacion['nombre_destinatario']}!</h2>
                <p>{datos_donacion['nombre_remitente']} ha realizado una donación.</p>

                <h3>Detalles de la donación:</h3>
                <ul>
                    <li>Categoría: {datos_donacion['categoria']}</li>
                    <li>Cantidad: {datos_donacion['cantidad']}</li>
                    <li>Descripción: {datos_donacion['descripcion']}</li>
                </ul>

                <h3>Detalles de la publicación:</h3>
                <p>{datos_donacion['mensaje_publicacion']}</p>

                <p>Puedes contactar al donante en: {datos_donacion['correo_remitente']}</p>

                <hr>
                <small>Este es un correo automático, por favor no responder directamente.</small>
            </body>
        </html>
        """

        payload = {
            "personalizations": [{
                "to": [{"email": datos_donacion["correo_destinatario"]}],
                "subject": "Has recibido una nueva donación"
            }],
            "from": {"email": self.correo_remitente},
            "content": [{
                "type": "text/html",
                "value": contenido_html
            }]
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.sendgrid.com/v3/mail/send",
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                )

            estado_envio = 'enviado' if response.status_code == 202 else 'fallido'
            detalles_error = None if response.status_code == 202 else f"Código de respuesta: {response.status_code}"

            registro = RegistroCorreo(
                donacion_id=datos_donacion['donacion_id'],
                destinatario=datos_donacion['correo_destinatario'],
                estado=estado_envio,
                id_mensaje=response.headers.get('X-Message-Id', ''),
                fecha_envio=datetime.now(),
                detalles_error=detalles_error
            )
            db.add(registro)
            db.commit()

            if response.status_code == 202:
                logger.info(f"Correo enviado. ID del mensaje: {registro.id_mensaje}")
                return {
                    "exitoso": True,
                    "mensaje": "Correo enviado y registrado correctamente",
                    "detalles": {
                        "id_registro": registro.id,
                        "id_mensaje": registro.id_mensaje,
                        "destinatario": registro.destinatario,
                        "estado": registro.estado,
                        "fecha_envio": registro.fecha_envio.isoformat()
                    }
                }
            else:
                raise HTTPException(status_code=500, detail=detalles_error)

        except Exception as e:
            logger.error(f"Error al enviar el correo: {str(e)}")
            registro_error = RegistroCorreo(
                donacion_id=datos_donacion['donacion_id'],
                destinatario=datos_donacion['correo_destinatario'],
                estado='fallido',
                fecha_envio=datetime.now(),
                detalles_error=str(e)
            )
            db.add(registro_error)
            db.commit()

            raise HTTPException(status_code=500, detail=f"Error al enviar el correo: {str(e)}")

    def _validar_datos_correo(self, datos: Dict) -> None:
        campos_requeridos = [
            'nombre_destinatario', 'correo_destinatario',
            'nombre_remitente', 'correo_remitente',
            'categoria', 'cantidad', 'descripcion',
            'mensaje_publicacion', 'donacion_id'
        ]

        for campo in campos_requeridos:
            if campo not in datos:
                raise ValueError(f"Campo requerido faltante: {campo}")
            if not datos[campo]:
                raise ValueError(f"El campo {campo} no puede estar vacío")

        if '@' not in datos['correo_destinatario'] or '.' not in datos['correo_destinatario']:
            raise ValueError("Formato de correo destinatario inválido")
        if '@' not in datos['correo_remitente'] or '.' not in datos['correo_remitente']:
            raise ValueError("Formato de correo remitente inválido")
