from domain.documento import Documento
from domain.errores import DocumentoNoEncontrado, TramiteFinalizado, TramiteNoEncontrado
from domain.tramite import EstadoTramite, Tramite
from repository.uow import AbstractUnitOfWork
from schemas.documento import DocumentoCrear


class DocumentoService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def crear(self, tramite_id: int, datos: DocumentoCrear) -> Documento:
        async with self._uow:
            await self._tramite_modificable(tramite_id)
            documento = Documento(
                nombre=datos.nombre,
                tipo=datos.tipo,
                tamanio=datos.tamanio,
                tramite_id=tramite_id,
            )
            return await self._uow.documentos.guardar(documento)

    async def listar_por_tramite(self, tramite_id: int) -> list[Documento]:
        async with self._uow:
            await self._tramite_existente(tramite_id)
            return await self._uow.documentos.listar_por_tramite(tramite_id)

    async def obtener(self, tramite_id: int, documento_id: int) -> Documento:
        async with self._uow:
            await self._tramite_existente(tramite_id)
            return await self._documento_del_tramite(tramite_id, documento_id)

    async def eliminar(self, tramite_id: int, documento_id: int) -> None:
        async with self._uow:
            await self._tramite_modificable(tramite_id)
            await self._documento_del_tramite(tramite_id, documento_id)
            await self._uow.documentos.eliminar(documento_id)

    # metodos privados
    async def _tramite_existente(self, tramite_id: int) -> Tramite:
        tramite = await self._uow.tramites.buscar(tramite_id)
        if tramite is None:
            raise TramiteNoEncontrado(tramite_id)
        return tramite

    async def _tramite_modificable(self, tramite_id: int) -> Tramite:
        tramite = await self._tramite_existente(tramite_id)
        if tramite.estado is EstadoTramite.FINALIZADO:
            raise TramiteFinalizado(tramite_id)
        return tramite

    async def _documento_del_tramite(self, tramite_id: int, documento_id: int) -> Documento:
        documento = await self._uow.documentos.buscar(documento_id)
        # Un documento de OTRO tramite se trata como inexistente
        if documento is None or documento.tramite_id != tramite_id:
            raise DocumentoNoEncontrado(documento_id)
        return documento
