from domain.errores import TramiteFinalizado, TramiteNoEncontrado
from domain.tramite import EstadoTramite, Tramite
from schemas.tramite import TramiteCrear
from repository.uow import AbstractUnitOfWork

ORDEN = list(EstadoTramite)

class TramiteService: 
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        # Inyeccion por constructur => el servicio no sabe QUE repositorio le dieron
        # solamente sabe que cumple con el Protocol.
        self._uow = uow

    async def crear(self, datos: TramiteCrear) -> Tramite: 
        async with self._uow:
            tramite = Tramite(**datos.model_dump())
            await self._uow.tramites.guardar(tramite)
            await self._uow.commit()
            return tramite

    async def listar(self, estado:EstadoTramite | None, skip:int, limit: int) -> list[Tramite]:
        async with self._uow:
            tramites = await self._uow.tramites.listar()
            if estado is not None:
                tramites = [t for t in tramites if t.estado == estado]
            return tramites[skip : skip + limit]

    async def obtener(self, tramite_id: int) -> Tramite | None:
        async with self._uow:
            return await self._uow.tramites.buscar(tramite_id)

    async def reemplazar(self, tramite_id: int, datos: TramiteCrear) -> Tramite:
        async with self._uow:
            tramite = await self._modificable_interno(tramite_id)
            tramite.tipo = datos.tipo
            tramite.cliente = datos.cliente
            tramite.monto = datos.monto
            await self._uow.tramites.guardar(tramite)
            await self._uow.commit()
            return tramite

# actualizar, eliminar TAREA

# metodos privados
    async def _obtener_interno(self, tramite_id: int) -> Tramite:
        tramite = await self._uow.tramites.buscar(tramite_id)
        if tramite is None:
            raise TramiteNoEncontrado(tramite_id)
        return tramite

    async def _modificable_interno(self, tramite_id:int) -> Tramite:
        tramite = await self._obtener_interno(tramite_id)
        if tramite.estado is EstadoTramite.FINALIZADO:
            raise TramiteFinalizado(tramite_id)
        return tramite