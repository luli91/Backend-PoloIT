from enum import Enum

class EstadoNombreEnum(str, Enum):
    Pendiente = "Pendiente"
    Entregado = "Entregado"
    Cancelado = "Cancelado"