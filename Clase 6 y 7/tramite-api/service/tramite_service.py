from domain.errores import TramiteFinalizado, TramiteNoEncontrado
from domain.tramite import EstadoTramite, Tramite
from repository.uow import AbstractUnitOfWork
from schemas.tramite import TramiteActualizar, TramiteCrear

ORDEN = list(EstadoTramite)


class TramiteService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        # Inyeccion por constructor => el servicio no sabe QUE repositorio le dieron
        # solamente sabe que cumple con el Protocol.
        self._uow = uow

    async def crear(self, datos: TramiteCrear) -> Tramite:
        async with self._uow:
            tramite = Tramite(**datos.model_dump())
            return await self._uow.tramites.guardar(tramite)

    async def listar(self, estado: EstadoTramite | None, skip: int, limit: int) -> list[Tramite]:
        async with self._uow:
            return await self._uow.tramites.listar(estado, skip, limit)

    async def obtener(self, tramite_id: int) -> Tramite:
        async with self._uow:
            return await self._obtener_interno(tramite_id)

    async def reemplazar(self, tramite_id: int, datos: TramiteCrear) -> Tramite:
        async with self._uow:
            tramite = await self._modificable_interno(tramite_id)
            tramite.tipo = datos.tipo
            tramite.cliente = datos.cliente
            tramite.monto = datos.monto
            return await self._uow.tramites.guardar(tramite)

    async def actualizar(self, tramite_id: int, datos: TramiteActualizar) -> Tramite:
        async with self._uow:
            tramite = await self._modificable_interno(tramite_id)
            # Solo los campos que el cliente mando (y que no vienen en null)
            cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
            for campo, valor in cambios.items():
                setattr(tramite, campo, valor)
            return await self._uow.tramites.guardar(tramite)

    async def eliminar(self, tramite_id: int) -> None:
        async with self._uow:
            await self._modificable_interno(tramite_id)
            await self._uow.tramites.eliminar(tramite_id)

    # metodos privados
    async def _obtener_interno(self, tramite_id: int) -> Tramite:
        tramite = await self._uow.tramites.buscar(tramite_id)
        if tramite is None:
            raise TramiteNoEncontrado(tramite_id)
        return tramite

    async def _modificable_interno(self, tramite_id: int) -> Tramite:
        tramite = await self._obtener_interno(tramite_id)
        if tramite.estado is EstadoTramite.FINALIZADO:
            raise TramiteFinalizado(tramite_id)
        return tramite
