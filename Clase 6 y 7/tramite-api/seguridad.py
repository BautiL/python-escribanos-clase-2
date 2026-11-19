"""Hash de contraseñas y tokens JWT. No sabe nada de FastAPI ni de la base."""

from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from config import variable_obligatoria

# Obligatoria: con una clave por defecto, cualquiera que lea el repo podria firmar tokens.
SECRET_KEY = variable_obligatoria("SECRET_KEY")
if len(SECRET_KEY.encode()) < 32:
    raise RuntimeError("SECRET_KEY debe tener al menos 32 bytes (HS256)")

ALGORITHM = "HS256"
EXPIRACION = timedelta(minutes=30)

_hasher = PasswordHash.recommended()  # Argon2


def hashear_password(password: str) -> str:
    return _hasher.hash(password)


def verificar_password(password: str, password_hash: str) -> bool:
    return _hasher.verify(password, password_hash)


def crear_token(email: str, expiracion: timedelta = EXPIRACION) -> str:
    ahora = datetime.now(UTC)
    payload = {"sub": email, "iat": ahora, "exp": ahora + expiracion}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def leer_token(token: str) -> str | None:
    """Devuelve el email del token, o None si es inválido o está vencido."""
    try:
        # require: un token sin "exp" no vale (si no, serviria para siempre)
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM], options={"require": ["exp", "sub"]}
        )
    except jwt.InvalidTokenError:  # firma inválida, vencido, mal formado, sin exp/sub...
        return None
    return payload["sub"]