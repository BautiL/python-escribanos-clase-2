from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.errores import TramiteNoEncontrado
from domain.tramite import EstadoTramite, Tramite
from repository.mappers.tramiteMapper import TramiteMapper
from repository.models.tramiteModel import TramiteModel


class RepositorioTramite(Protocol):
    # El "contrato" (la interface de "Java")
    async def guardar(self, tramite: Tramite) -> Tramite: ...
    async def buscar(self, tramite_id: int) -> Tramite | None: ...
    async def listar(
        self, estado: EstadoTramite | None = None, skip: int = 0, limit: int | None = None
    ) -> list[Tramite]: ...
    async def eliminar(self, tramite_id: int) -> None: ...


class RepositorioTramiteSqlalchemy:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def guardar(self, tramite: Tramite) -> Tramite:
        if tramite.id is None:
            # Alta: INSERT del tramite (y de sus documentos, si trae)
            tramite_model = TramiteMapper.to_model(tramite)
            self.session.add(tramite_model)
            await self.session.flush()
            tramite.id = tramite_model.id
            for documento, documento_model in zip(tramite.documentos, tramite_model.documentos):
                documento.id = documento_model.id
                documento.tramite_id = tramite_model.id
            return tramite

        # Modificacion: se actualiza el modelo ya persistido (no se crea uno nuevo
        # con el mismo id, eso provocaba un INSERT duplicado).
        tramite_model = await self.session.get(TramiteModel, tramite.id)
        if tramite_model is None:
            raise TramiteNoEncontrado(tramite.id)
        tramite_model.tipo = tramite.tipo
        tramite_model.cliente = tramite.cliente
        tramite_model.monto = tramite.monto
        tramite_model.estado = tramite.estado
        await self.session.flush()
        return tramite

    async def eliminar(self, tramite_id: int) -> None:
        tramite = await self.session.get(TramiteModel, tramite_id)
        if tramite is None:
            raise TramiteNoEncontrado(tramite_id)
        await self.session.delete(tramite)
        await self.session.flush()

    async def buscar(self, tramite_id: int) -> Tramite | None:
        tramite_model = await self.session.get(TramiteModel, tramite_id)
        if tramite_model is None:
            return None
        return TramiteMapper.to_domain(tramite_model)

    async def listar(
        self, estado: EstadoTramite | None = None, skip: int = 0, limit: int | None = None
    ) -> list[Tramite]:
        # El filtro y la paginacion se hacen en la base, no en memoria
        query = select(TramiteModel).order_by(TramiteModel.id)
        if estado is not None:
            query = query.where(TramiteModel.estado == estado)
        query = query.offset(skip)
        if limit is not None:
            query = query.limit(limit)
        result = await self.session.execute(query)
        return [TramiteMapper.to_domain(tramite_model) for tramite_model in result.scalars().all()]
