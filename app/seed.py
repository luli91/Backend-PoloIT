from sqlalchemy.orm import Session
from app.models.estado import Estado
from app.models.categoria import Categoria
from app.utils.estado_nombre import EstadoNombreEnum
from app.database import SessionLocal

def cargar_estados(db: Session):
    print("Ejecutando seed de estados...")
    ya_existen = db.query(Estado).count()
    if ya_existen > 0:
        print("Estados ya existen, no se vuelve a cargar.")
        return

    for estado in EstadoNombreEnum:
        db.add(Estado(nombre=estado.value))

    db.commit()
    print("Estados cargados correctamente.")

def cargar_categorias(db: Session):
    print("Cargando categorías...")
    categorias = [
        "Ropa", "Libros", "Muebles", "Alimentos",
        "Servicios", "Electrónica", "Juguetes"
    ]
    if db.query(Categoria).count() > 0:
        print("Ya existen categorías, se omite carga.")
        return
    for nombre in categorias:
        db.add(Categoria(nombre=nombre))
    db.commit()
    print("Categorías cargadas correctamente.")

# Permite correr el seed directamente
if __name__ == "__main__":
    db = SessionLocal()
    cargar_estados(db)
    cargar_categorias(db)
    db.close()