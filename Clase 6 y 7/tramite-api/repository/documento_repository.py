from typing import Protocol 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from domain.documento import Documento
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
        documento_model = DocumentoMapper.to_model(documento)
        await self.session.merge(documento_model)
        await self.session.flush()
        documento.id = documento_model.id
        documento.tramite_id = documento_model.tramite_id
        return documento

    async def buscar(self, documento_id: int) -> Documento | None:
        documento_model = await self.session.get(DocumentoModel, documento_id)
        if documento_model is None:
            return None
        return DocumentoMapper.to_domain(documento_model)

    async def listar(self) -> list[Documento]:
        query = select(DocumentoModel)
        result = await self.session.execute(query)
        return [
            DocumentoMapper.to_domain(documento_model)
            for documento_model in result.scalars().all()
        ]

    async def listar_por_tramite(self, tramite_id: int) -> list[Documento]:
        query = select(DocumentoModel).where(DocumentoModel.tramite_id == tramite_id)
        result = await self.session.execute(query)
        return [
            DocumentoMapper.to_domain(documento_model)
            for documento_model in result.scalars().all()
        ]

    async def eliminar(self, documento_id: int) -> None:
        documento = await self.session.get(DocumentoModel, documento_id)
        if documento is None:
            raise ValueError("El documento a eliminar no existe")
        await self.session.delete(documento)