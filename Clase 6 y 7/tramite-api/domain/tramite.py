from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.documento import Documento


class EstadoTramite(StrEnum):
    # estos son los estados del tramite
    # estos estados son de tipo string
    INICIADO = "iniciado"
    EN_FIRMA = "en_firma"
    FINALIZADO = "finalizado"


@dataclass
class Tramite:
    tipo: str
    cliente: str
    monto: float
    estado: EstadoTramite = EstadoTramite.INICIADO
    id: int | None = None
    documentos: list[Documento] = field(default_factory=list)