from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Publicacion(Base):
    __tablename__ = "publicacion"

    id = Column(Integer, primary_key=True, index=True)
    mensaje = Column(String)
    donacion_id = Column(Integer, ForeignKey("donacion.id"))
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    estado_id = Column(Integer, ForeignKey("estado.id"))

    estado = relationship("Estado", back_populates="publicaciones")
    donacion = relationship("Donacion", back_populates="publicaciones")
    usuario = relationship("Usuario")