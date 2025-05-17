from enum import Enum

class EstadoNombre(str, Enum):
    Activo = "Activo"
    Entregado = "Entregado"
    Cancelado = "Cancelado"