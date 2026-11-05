from typing import Protocol 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from domain.tramite import Tramite
from repository.mappers.tramiteMapper import TramiteMapper
from repository.models.tramiteModel import TramiteModel

class RepositorioTramite(Protocol): 
    # El "contrato" (la interface de "Java")
    async def guardar(self, tramite: Tramite) -> Tramite: ...
    async def buscar(self, tramite_id: int) -> Tramite | None: ...
    async def listar(self) -> list[Tramite]: ...
    async def eliminar(self, tramite_id: int) -> None: ...

class RepositorioTramiteSqlalchemy: 
    def __init__(self, session: AsyncSession):
        self.session = session

    async def guardar(self, tramite: Tramite) -> Tramite: 
        tramite_model = TramiteMapper.to_model(tramite)
        await self.session.merge(tramite_model)
        await self.session.flush()
        tramite.id = tramite_model.id
        return tramite

    async def eliminar(self, tramite_id: int) -> None:
        tramite = await self.session.get(TramiteModel, tramite_id)
        if tramite:
            await self.session.delete(tramite)
        else:
            raise ValueError('El tramite a eliminar no existe')

    async def buscar(self, tramite_id: int) -> Tramite | None:
        query = select(TramiteModel).where(TramiteModel.id == tramite_id)
        result = await self.session.execute(query)
        tramite_model = result.scalar()

        if tramite_model is None:
            return None
        return TramiteMapper.to_domain(tramite_model)

    async def listar(self) -> list[Tramite]:
        query = select(TramiteModel)
        result = await self.session.execute(query)
        return [TramiteMapper.to_domain(tramite_model) for tramite_model in result.scalars().all()]
    