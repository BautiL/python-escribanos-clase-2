from typing import Protocol, Self
from types import TracebackType
from repository.tramite_repository import RepositorioTramite, RepositorioTramiteSqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

class AbstractUnitOfWork(Protocol):
    tramites: RepositorioTramite

    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type:type[BaseException], exc_val:BaseException | None, 
                        exc_tb: TracebackType | None) -> None:...
    async def commit(self)->None: ...
    async def rollback(self)->None: ...

class SqlAlchemyUnitOfWork:
    tramites: RepositorioTramite

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()

        self.tramites= RepositorioTramiteSqlalchemy(self.session)
        return self

    async def __aexit__(self, exc_type:type[BaseException], exc_val:BaseException | None, 
                            exc_tb: TracebackType | None) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()