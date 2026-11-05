from domain.documento import Documento
from domain.errores import TramiteNoEncontrado
from repository.uow import AbstractUnitOfWork
from schemas.documento import DocumentoCrear


class DocumentoService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def crear(self, tramite_id: int, datos: DocumentoCrear) -> Documento:
        async with self._uow:
            tramite = await self._uow.tramites.buscar(tramite_id)
            if tramite is None:
                raise TramiteNoEncontrado(tramite_id)

            documento = Documento(
                nombre=datos.nombre,
                tipo=datos.tipo,
                tamanio=datos.tamanio,
                tramite_id=tramite_id,
            )
            return await self._uow.documentos.guardar(documento)

    async def listar_por_tramite(self, tramite_id: int) -> list[Documento]:
        async with self._uow:
            return await self._uow.documentos.listar_por_tramite(tramite_id)

    async def obtener(self, documento_id: int) -> Documento | None:
        async with self._uow:
            return await self._uow.documentos.buscar(documento_id)

    async def eliminar(self, documento_id: int) -> None:
        async with self._uow:
            await self._uow.documentos.eliminar(documento_id)
