from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.provincias import ProvinciaEnum  # ✅ Import correcto

class Ubicacion(Base):
    __tablename__ = "ubicacion"

    id = Column(Integer, primary_key=True, index=True)
    direccion = Column(String)
    codigo_postal = Column(String)
    ciudad = Column(String)
    provincia = Column(SQLEnum(ProvinciaEnum, name="provincia_enum"), nullable=False)

    usuarios = relationship("Usuario", back_populates="ubicacion")