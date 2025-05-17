from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.models.estado import Estado, EstadoNombreEnum


def cargar_categorias(db: Session):
    categorias = [
        "Ropa", "Libros", "Muebles", "Alimentos", "Servicios", "Electrónica", "Juguetes"
    ]
    
    for nombre in categorias:
        ya_existe = db.query(Categoria).filter_by(nombre=nombre).first()
        if not ya_existe:
            db.add(Categoria(nombre=nombre))
    
    db.commit()


def cargar_estados(db: Session):
    for estado_enum in EstadoNombreEnum:
        nombre_estado = estado_enum.value  # siempre usar .value
        ya_existe = db.query(Estado).filter_by(nombre=nombre_estado).first()
        if not ya_existe:
            db.add(Estado(nombre=nombre_estado))
    
    db.commit()
    
# Evitar que se ejecute al importar desde uvicorn
if __name__ == "__main__":
    from app.database import SessionLocal

    db = SessionLocal()
    cargar_estados(db)
    cargar_categorias(db)
    db.close()