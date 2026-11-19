from domain.errores import CredencialesInvalidas, EmailYaRegistrado
from domain.usuario import Usuario
from repository.uow import AbstractUnitOfWork
from schemas.usuario import UsuarioCrear
from seguridad import crear_token, hashear_password, leer_token, verificar_password


class AuthService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def registrar(self, datos: UsuarioCrear) -> Usuario:
        async with self._uow:
            if await self._uow.usuarios.buscar_por_email(datos.email) is not None:
                raise EmailYaRegistrado(datos.email)
            usuario = Usuario(
                email=datos.email,
                nombre=datos.nombre,
                password_hash=hashear_password(datos.password),
            )
            return await self._uow.usuarios.guardar(usuario)

    async def login(self, email: str, password: str) -> str:
        async with self._uow:
            usuario = await self._uow.usuarios.buscar_por_email(email)
        # Mismo error si el email no existe o la contraseña no coincide
        if usuario is None or not verificar_password(password, usuario.password_hash):
            raise CredencialesInvalidas()
        if not usuario.activo:
            raise CredencialesInvalidas()
        return crear_token(usuario.email)

    async def usuario_del_token(self, token: str) -> Usuario:
        email = leer_token(token)
        if email is None:
            raise CredencialesInvalidas()
        async with self._uow:
            usuario = await self._uow.usuarios.buscar_por_email(email)
        if usuario is None or not usuario.activo:
            raise CredencialesInvalidas()
        return usuario