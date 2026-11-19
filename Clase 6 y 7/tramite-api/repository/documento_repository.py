from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.documento import Documento
from domain.errores import DocumentoNoEncontrado
from repository.mappers.documentoMapper import DocumentoMapper
from repository.models.documentoModel import DocumentoModel


class RepositorioDocumento(Protocol):
    async def guardar(self, documento: Documento) -> Documento: ...
    async def buscar(self, documento_id: int) -> Documento | None: ...
    async def listar(self) -> list[Documento]: ...
    async def eliminar(self, documento_id: int) -> None: ...
    async def listar_por_tramite(self, tramite_id: int) -> list[Documento]: ...


class RepositorioDocumentoSqlalchemy:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def guardar(self, documento: Documento) -> Documento:
        if documento.id is None:
            documento_model = DocumentoMapper.to_model(documento)
            self.session.add(documento_model)
            await self.session.flush()
            documento.id = documento_model.id
            documento.tramite_id = documento_model.tramite_id
            return documento

        documento_model = await self.session.get(DocumentoModel, documento.id)
        if documento_model is None:
            raise DocumentoNoEncontrado(documento.id)
        documento_model.nombre = documento.nombre
        documento_model.tipo = documento.tipo
        documento_model.tamanio = documento.tamanio
        await self.session.flush()
        return documento

    async def buscar(self, documento_id: int) -> Documento | None:
        documento_model = await self.session.get(DocumentoModel, documento_id)
        if documento_model is None:
            return None
        return DocumentoMapper.to_domain(documento_model)

    async def listar(self) -> list[Documento]:
        query = select(DocumentoModel).order_by(DocumentoModel.id)
        result = await self.session.execute(query)
        return [DocumentoMapper.to_domain(m) for m in result.scalars().all()]

    async def listar_por_tramite(self, tramite_id: int) -> list[Documento]:
        query = (
            select(DocumentoModel)
            .where(DocumentoModel.tramite_id == tramite_id)
            .order_by(DocumentoModel.id)
        )
        result = await self.session.execute(query)
        return [DocumentoMapper.to_domain(m) for m in result.scalars().all()]

    async def eliminar(self, documento_id: int) -> None:
        documento = await self.session.get(DocumentoModel, documento_id)
        if documento is None:
            raise DocumentoNoEncontrado(documento_id)
        await self.session.delete(documento)
        await self.session.flush()
