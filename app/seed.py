from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.models.estado import Estado, EstadoNombreEnum
from app.database import SessionLocal

def cargar_categorias(db: Session):
    ya_existen = db.query(Categoria).count()
    if ya_existen > 0:
        return

    categorias = [
        "Ropa", "Libros", "Muebles", "Alimentos",
        "Servicios", "Electrónica", "Juguetes"
    ]

    for nombre in categorias:
        db.add(Categoria(nombre=nombre))

    db.commit()

def cargar_estados(db: Session):
    print("💡 Ejecutando seed de estados...")  # 👈 DEBUG
    ya_existen = db.query(Estado).count()
    if ya_existen > 0:
        print("✅ Estados ya existen, no se vuelve a cargar.")
        return

    estados = ["Pendiente", "Entregado", "Cancelado"]
    for nombre in estados:
        db.add(Estado(nombre=nombre))

    db.commit()
    print("✅ Estados cargados correctamente.")

# Permite ejecutar el seed directamente con: python app/seed.py
if __name__ == "__main__":
    db = SessionLocal()
    cargar_estados(db)
    cargar_categorias(db)
    db.close()