from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from repository.database import async_session_maker
from repository.uow import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from service.documento_service import DocumentoService
from service.tramite_service import TramiteService

from domain.usuario import Usuario
from service.auth_service import AuthService


def get_uow() -> AbstractUnitOfWork:
    return SqlAlchemyUnitOfWork(async_session_maker)


UoWDep = Annotated[AbstractUnitOfWork, Depends(get_uow)]


def get_service(uow: UoWDep) -> TramiteService:
    return TramiteService(uow)


def get_documento_service(uow: UoWDep) -> DocumentoService:
    return DocumentoService(uow)

def get_auth_service(uow: UoWDep) -> AuthService:
    return AuthService(uow)


ServiceDep = Annotated[TramiteService, Depends(get_service)]
DocumentoServiceDep = Annotated[DocumentoService, Depends(get_documento_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

# Lee el header "Authorization: Bearer <token>". Si no está, responde 401 solo.
# tokenUrl es para Swagger: ahí manda el formulario del botón "Authorize".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_usuario_actual(
    token: Annotated[str, Depends(oauth2_scheme)], service: AuthServiceDep
) -> Usuario:
    return await service.usuario_del_token(token)  # CredencialesInvalidas -> 401


UsuarioActual = Annotated[Usuario, Depends(get_usuario_actual)]