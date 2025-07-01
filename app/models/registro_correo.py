# app/models/registro_correo.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class RegistroCorreo(Base):
    __tablename__ = "registros_correo"

    id = Column(Integer, primary_key=True, index=True)
    donacion_id = Column(Integer, ForeignKey("donacion.id", ondelete="CASCADE"))
    destinatario = Column(String)
    estado = Column(String)
    id_mensaje = Column(String, nullable=True)
    fecha_envio = Column(DateTime)
    detalles_error = Column(String, nullable=True)

    # Opcional: agregar relación con la tabla donaciones
    donacion = relationship("Donacion", back_populates="registros_correo")