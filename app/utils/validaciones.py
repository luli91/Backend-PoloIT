from app.utils.provincias import PROVINCIAS_ARGENTINAS

def validar_provincia(provincia: str) -> bool:
    return provincia.strip().title() in PROVINCIAS_ARGENTINAS