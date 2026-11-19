import os

from dotenv import load_dotenv

# No pisa variables que ya esten definidas en el entorno.
load_dotenv()


def variable_obligatoria(nombre: str) -> str:
    """Devuelve la variable de entorno o corta el arranque si falta.

    Mejor que la app no arranque a que arranque con un valor inseguro por defecto.
    """
    valor = os.getenv(nombre)
    if not valor:
        raise RuntimeError(f"Falta la variable de entorno {nombre} (ver .env.example)")
    return valor