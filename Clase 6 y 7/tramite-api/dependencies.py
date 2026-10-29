from repository.uow import SqlAlchemyUnitOfWork, AbstractUnitOfWork
from repository.database import async_session_maker
from fastapi import Depends
from service.tramite_service import TramiteService
from typing import Annotated

def get_uow() -> AbstractUnitOfWork:
    return SqlAlchemyUnitOfWork(async_session_maker)

def get_service(uow: Annotated[AbstractUnitOfWork, Depends(get_uow)]) -> TramiteService:
    return TramiteService(uow)

ServiceDep = Annotated[TramiteService, Depends(get_service)]
UoWDep = Annotated[AbstractUnitOfWork, Depends(get_uow)]