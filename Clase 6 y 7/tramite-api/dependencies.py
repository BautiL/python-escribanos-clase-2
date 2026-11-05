from typing import Annotated

from fastapi import Depends

from repository.database import async_session_maker
from repository.uow import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from service.documento_service import DocumentoService
from service.tramite_service import TramiteService


def get_uow() -> AbstractUnitOfWork:
    return SqlAlchemyUnitOfWork(async_session_maker)


def get_service(uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]) -> TramiteService:
    return TramiteService(uow)


def get_documento_service(uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]) -> DocumentoService:
    return DocumentoService(uow)


ServiceDep = Annotated[TramiteService, Depends(get_service)]
DocumentoServiceDep = Annotated[DocumentoService, Depends(get_documento_service)]
UoWDep = Annotated[AbstractUnitOfWork, Depends(get_uow)]