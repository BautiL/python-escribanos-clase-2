from domain.usuario import Usuario
from repository.models.usuarioModel import UsuarioModel


class UsuarioMapper:
    @staticmethod
    def to_model(usuario: Usuario) -> UsuarioModel:
        return UsuarioModel(
            id=usuario.id,
            email=usuario.email,
            nombre=usuario.nombre,
            password_hash=usuario.password_hash,
            activo=usuario.activo,
        )

    @staticmethod
    def to_domain(model: UsuarioModel) -> Usuario:
        return Usuario(
            id=model.id,
            email=model.email,
            nombre=model.nombre,
            password_hash=model.password_hash,
            activo=model.activo,
        )