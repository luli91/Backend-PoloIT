from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Estado(Base):
    __tablename__ = "estado"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)

    donaciones = relationship("Donacion", back_populates="estado")