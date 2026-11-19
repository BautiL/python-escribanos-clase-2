from types import TracebackType
from typing import Protocol, Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from repository.documento_repository import RepositorioDocumento, RepositorioDocumentoSqlalchemy
from repository.tramite_repository import RepositorioTramite, RepositorioTramiteSqlalchemy
from repository.usuario_repository import RepositorioUsuario, RepositorioUsuarioSqlalchemy


class AbstractUnitOfWork(Protocol):
    tramites: RepositorioTramite
    documentos: RepositorioDocumento
    usuarios: RepositorioUsuario

    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...


class SqlAlchemyUnitOfWork:
    tramites: RepositorioTramite
    documentos: RepositorioDocumento
    usuarios: RepositorioUsuario

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> Self:
        # La misma instancia se comparte en un request (FastAPI cachea get_uow).
        # Usarla anidada pisaria la sesion abierta: mejor fallar fuerte.
        if self.session is not None:
            raise RuntimeError("El Unit of Work ya esta en uso (no se puede anidar)")
        self.session = self.session_factory()
        self.tramites = RepositorioTramiteSqlalchemy(self.session)
        self.documentos = RepositorioDocumentoSqlalchemy(self.session)
        self.usuarios = RepositorioUsuarioSqlalchemy(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            # Se cierra la sesion aunque el commit falle
            await self._sesion_activa().close()
            self.session = None

    async def commit(self) -> None:
        await self._sesion_activa().commit()

    async def rollback(self) -> None:
        await self._sesion_activa().rollback()

    def _sesion_activa(self) -> AsyncSession:
        if self.session is None:
            raise RuntimeError("El Unit of Work no esta abierto (usar 'async with')")
        return self.session
