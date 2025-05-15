from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Donacion(Base):
    __tablename__ = "donacion"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)    
    cantidad = Column(Integer, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    publicaciones = relationship("Publicacion", back_populates="donacion")