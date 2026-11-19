import os

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from domain.errores import DocumentoNoEncontrado, TramiteFinalizado, TramiteNoEncontrado, CredencialesInvalidas, EmailYaRegistrado
from routers import documento_router, tramite_router, auth_router

# debug solo si se pide explicitamente: DEBUG=1
app = FastAPI(title="Gestion de tramites", debug=os.getenv("DEBUG") == "1")
app.include_router(tramite_router.router)
app.include_router(documento_router.router)
app.include_router(auth_router.router)


def _manejador(status_code: int, headers: dict[str, str] | None = None):
    async def manejar(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": str(exc)}, headers=headers)

    return manejar


# Errores del dominio -> codigos HTTP (sin esto la API respondia 500)
app.add_exception_handler(TramiteNoEncontrado, _manejador(status.HTTP_404_NOT_FOUND))
app.add_exception_handler(DocumentoNoEncontrado, _manejador(status.HTTP_404_NOT_FOUND))
app.add_exception_handler(TramiteFinalizado, _manejador(status.HTTP_409_CONFLICT))
app.add_exception_handler(EmailYaRegistrado, _manejador(status.HTTP_409_CONFLICT))
app.add_exception_handler(CredencialesInvalidas, _manejador(status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"}))
