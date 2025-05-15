from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Donacion(Base):
    __tablename__ = "publicacion"

    id = Column(Integer, primary_key=True, index=True)
    donacion_id = Column(Integer, ForeignKey("donacion.id"), nullable=False)    
    imagen_url = Column(String, nullable=True)
    estado_id = Column(Integer, ForeignKey("estado.id"), nullable=False)
    fecha_publicacion = Column(DateTime, default=datetime.utcnow)
    visible = Column(Boolean, default=True)

    donacion = relationship("Donacion", back_populates="publicaciones")