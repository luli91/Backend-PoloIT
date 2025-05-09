from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Ubicacion(Base):
    __tablename__ = "ubicacion"

    id = Column(Integer, primary_key=True, index=True)
    direccion = Column(String)
    codigo_postal = Column(String)
    ciudad = Column(String)
    provincia = Column(String)

    usuarios = relationship("Usuario", back_populates="ubicacion")