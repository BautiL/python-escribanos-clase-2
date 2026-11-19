from dataclasses import dataclass


@dataclass
class Documento:
    nombre: str
    tipo: str
    tramite_id: int | None = None
    id: int | None = None
    tamanio: int | None = None
