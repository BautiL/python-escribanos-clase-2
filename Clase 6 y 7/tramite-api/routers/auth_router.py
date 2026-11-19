from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import AuthServiceDep, UsuarioActual
from schemas.usuario import Token, UsuarioCrear, UsuarioRespuesta

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/registro", status_code=status.HTTP_201_CREATED)
async def registrar(datos: UsuarioCrear, service: AuthServiceDep) -> UsuarioRespuesta:
    return UsuarioRespuesta.model_validate(await service.registrar(datos))


@router.post("/token")
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], service: AuthServiceDep
) -> Token:
    # OAuth2 manda un formulario (no JSON) con "username" y "password".
    # Nuestro username es el email.
    return Token(access_token=await service.login(form.username, form.password))


@router.get("/yo")
async def yo(usuario: UsuarioActual) -> UsuarioRespuesta:
    return UsuarioRespuesta.model_validate(usuario)