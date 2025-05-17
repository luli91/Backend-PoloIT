from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Publicacion(Base):
    __tablename__ = "publicacion"

    id = Column(Integer, primary_key=True, index=True)
    mensaje = Column(String)
    donacion_id = Column(Integer, ForeignKey("donacion.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    estado_id = Column(Integer, ForeignKey("estado.id"), nullable=False)

    estado = relationship("Estado", back_populates="publicaciones")
    donacion = relationship("Donacion", back_populates="publicaciones")
    usuario = relationship("Usuario")