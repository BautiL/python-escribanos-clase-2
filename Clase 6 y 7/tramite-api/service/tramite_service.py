from domain.errores import TramiteFinalizado, TramiteNoEncontrado
from domain.tramite import EstadoTramite, Tramite
from repository.uow import AbstractUnitOfWork
from schemas.tramite import TramiteActualizar, TramiteCrear


class TramiteService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        # Inyeccion por constructor => el servicio no sabe QUE repositorio le dieron
        # solamente sabe que cumple con el Protocol.
        self._uow = uow

    async def crear(self, datos: TramiteCrear, usuario_id: int) -> Tramite:
        async with self._uow:
            tramite = Tramite(**datos.model_dump(), usuario_id = usuario_id)
            return await self._uow.tramites.guardar(tramite)

    async def listar(self, usuario_id: int, estado: EstadoTramite | None, skip: int, limit: int) -> list[Tramite]:
        async with self._uow:
            return await self._uow.tramites.listar(usuario_id, estado, skip, limit)

    async def obtener(self, tramite_id: int, usuario_id: int) -> Tramite:
        async with self._uow:
            return await self._obtener_interno(tramite_id, usuario_id)

    async def reemplazar(self, tramite_id: int, datos: TramiteCrear, usuario_id: int) -> Tramite:
        async with self._uow:
            tramite = await self._modificable_interno(tramite_id, usuario_id)
            tramite.tipo = datos.tipo
            tramite.cliente = datos.cliente
            tramite.monto = datos.monto
            return await self._uow.tramites.guardar(tramite)

    async def actualizar(self, tramite_id: int, datos: TramiteActualizar, usuario_id: int) -> Tramite:
        async with self._uow:
            tramite = await self._modificable_interno(tramite_id, usuario_id)
            # Solo los campos que el cliente mando (y que no vienen en null)
            cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
            for campo, valor in cambios.items():
                setattr(tramite, campo, valor)
            return await self._uow.tramites.guardar(tramite)

    async def eliminar(self, tramite_id: int, usuario_id: int) -> None:
        async with self._uow:
            await self._modificable_interno(tramite_id, usuario_id)
            await self._uow.tramites.eliminar(tramite_id)

    # metodos privados
    async def _obtener_interno(self, tramite_id: int, usuario_id: int) -> Tramite:
        tramite = await self._uow.tramites.buscar(tramite_id)
        if tramite is None or tramite.usuario_id != usuario_id:
            raise TramiteNoEncontrado(tramite_id)
        return tramite

    async def _modificable_interno(self, tramite_id: int, usuario_id: int) -> Tramite:
        tramite = await self._obtener_interno(tramite_id, usuario_id)
        if tramite.estado is EstadoTramite.FINALIZADO:
            raise TramiteFinalizado(tramite_id)
        return tramite
