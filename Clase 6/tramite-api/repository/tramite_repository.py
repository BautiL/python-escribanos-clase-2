from typing import Protocol 

from domain.tramite import Tramite

class RepositorioTramite(Protocol): 
    # El "contrato" (la interface de "Java")
    def siguiente_id(self) -> int: ...
    def guardar(self, tramite: Tramite) -> None: ...
    def buscar(self, tramite_id: int) -> Tramite | None: ...
    def listar(self) -> list[Tramite]: ...
    def eliminar(self, tramite_id: int) -> None: ...

class RepositorioEnMemoria: 
    def __init__(self) -> None:
        self._datos: dict[int, Tramite] = {} # id -> tramite
        self._ultimo_id = 0 # "autoincrementar" casero

    def siguiente_id(self) -> int:
        self._ultimo_id += 1
        return self._ultimo_id

    def guardar(self, tramite: Tramite) -> None: 
        self._datos[tramite.id] = tramite # si ya existia, lo pisa (sirve para el update)

    def eliminar(self, tramite_id: int) -> None:
        self._datos.pop(tramite_id, None) # el None evita error si ya no estaba / existia

    # TAREA!!!!!!!
    def buscar(self, tramite_id: int) -> Tramite | None:
        pass

    def listar(self) -> list[Tramite]:
        pass

    