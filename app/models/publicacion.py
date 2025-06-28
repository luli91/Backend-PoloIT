from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Publicacion(Base):
    __tablename__ = "publicacion"

    id = Column(Integer, primary_key=True, index=True)
    mensaje = Column(String, nullable=False, default="")
    donacion_id = Column(Integer, ForeignKey("donacion.id"), nullable=False, unique=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    estado_id = Column(Integer, ForeignKey("estado.id"), nullable=False)
    imagen_url = Column(String, nullable=True)
    visible = Column(Boolean, default=True)
    fecha_publicacion = Column(DateTime, default=datetime.utcnow)

    donacion = relationship("Donacion", back_populates="publicaciones")
    usuario = relationship("Usuario", back_populates="publicaciones")
    estado = relationship("Estado", back_populates="publicaciones")

    @property
    def estado_nombre(self) -> str:
        return self.estado.nombre
