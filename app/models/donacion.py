from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Donacion(Base):
    __tablename__ = "donacion"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    cantidad = Column(Float)
    imagen_url = Column(String)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    categoria_id = Column(Integer, ForeignKey("categoria.id"))
    estado_id = Column(Integer, ForeignKey("estado.id"))

    usuario = relationship("Usuario", back_populates="donaciones")
    categoria = relationship("Categoria", back_populates="donaciones")
    estado = relationship("Estado", back_populates="donaciones")