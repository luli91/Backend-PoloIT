from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Ubicacion(Base):
    __tablename__ = "ubicacion"

    id = Column(Integer, primary_key=True, index=True)
    direccion = Column(String, nullable=False)
    codigo_postal = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    provincia = Column(String, nullable=False)

    usuarios = relationship("Usuario", back_populates="ubicacion")