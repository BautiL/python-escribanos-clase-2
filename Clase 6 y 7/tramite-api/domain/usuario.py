from dataclasses import dataclass


@dataclass
class Usuario:
    email: str
    nombre: str
    password_hash: str  # nunca la contraseña: solo su hash
    activo: bool = True
    id: int | None = None