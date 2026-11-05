from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.tramite import Tramite


@dataclass
class Documento:
    nombre: str
    tipo: str
    tramite_id: int | None = None
    id: int | None = None
    tamanio: int | None = None
    tramite: "Tramite | None" = None
