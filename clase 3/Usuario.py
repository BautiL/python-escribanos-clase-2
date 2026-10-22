from dataclasses import dataclass
from datetime import datetime

from Estado import Estado
from Rol import Rol

type FechaNula = datetime | None

@dataclass
class Usuario:
    id: int 
    mail:str
    nombre: str
    contraseña: str
    roles: list[Rol]
    estado: Estado
    fecha_creacion: datetime
    intentos_fallidos_login: int = 0
    ultimo_login: FechaNula = None
    fecha_suspension: FechaNula = None

    def activar(self):
        if self.estado == Estado.ACTIVO:
            raise ValueError('El usuario ya está activo')

        self.estado = Estado.ACTIVO

    def suspender(self):
        self.estado = Estado.SUSPENDIDO
        self.fecha_suspension = datetime.now()

    def puedeIngresar(self):
        return self.estado == Estado.ACTIVO