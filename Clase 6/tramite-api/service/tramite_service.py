from domain.errores import TramiteFinalizado, TramiteNoEncontrado
from domain.tramite import EstadoTramite, Tramite
from repository.tramite_repository import RepositorioTramite
from schemas.tramite import TramiteActualizar, TramiteCrear

ORDEN = list(EstadoTramite)

class TramiteService: 
    def __init__(self, repo: RepositorioTramite) -> None:
        # Inyeccion por constructur => el servicio no sabe QUE repositorio le dieron
        # solamente sabe que cumple con el Protocol.
        self._repo = repo

    def crear(self, datos: TramiteCrear) -> Tramite: 
        tramite = Tramite(id=self._repo.siguiente_id(), **datos.model_dump())
        self._repo.guardar(tramite)
        return tramite

    # TAREA