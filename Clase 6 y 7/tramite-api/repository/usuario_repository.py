from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.usuario import Usuario
from repository.mappers.usuarioMapper import UsuarioMapper
from repository.models.usuarioModel import UsuarioModel


class RepositorioUsuario(Protocol):
    async def guardar(self, usuario: Usuario) -> Usuario: ...
    async def buscar_por_email(self, email: str) -> Usuario | None: ...


class RepositorioUsuarioSqlalchemy:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def guardar(self, usuario: Usuario) -> Usuario:
        model = UsuarioMapper.to_model(usuario)
        self.session.add(model)
        await self.session.flush()
        usuario.id = model.id
        return usuario

    async def buscar_por_email(self, email: str) -> Usuario | None:
        query = select(UsuarioModel).where(UsuarioModel.email == email)
        model = (await self.session.execute(query)).scalar_one_or_none()
        return UsuarioMapper.to_domain(model) if model else None