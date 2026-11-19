class TramiteError(Exception):
    """Base de todos los errores del dominio (sirva para atraparlos a todos juntos)"""

class TramiteNoEncontrado(TramiteError):
    def __init__(self, tramite_id: int) -> None:
        super().__init__(f"No existe el tramite {tramite_id}")
        self.tramite_id = tramite_id

class TramiteFinalizado(TramiteError):
    def __init__(self, tramite_id: int) -> None:
        super().__init__(f"El tramite {tramite_id} esta finalizado y no se puede modificar")
        self.tramite_id = tramite_id


class DocumentoNoEncontrado(TramiteError):
    def __init__(self, documento_id: int) -> None:
        super().__init__(f"No existe el documento {documento_id}")
        self.documento_id = documento_id

class CredencialesInvalidas(Exception):
    """Email o contraseña incorrectos, o token inválido o vencido.

    El mensaje es el mismo en todos los casos a propósito: no le decimos a un atacante
    si el email existe.
    """

    def __init__(self) -> None:
        super().__init__("Credenciales inválidas")

class EmailYaRegistrado(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"Ya existe un usuario con el email {email}")
        self.email = email