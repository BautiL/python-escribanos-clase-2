from dataclasses import dataclass
from enum import StrEnum

class EstadoTramite(StrEnum):
    # estos son los estados del tramite
    # estos estados son de tipo string
    INICIADO = "iniciado"
    EN_FIRMA = "en_firma"
    FINALIZADO = "finalizado"

@dataclass
class Tramite: 
    id: int 
    tipo: str
    cliente: str 
    monto: float
    estado: EstadoTramite = EstadoTramite.INICIADO