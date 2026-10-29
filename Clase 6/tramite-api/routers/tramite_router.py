from typing import Annotated

from fastapi import APIRouter, Query

from dependencies import ServiceDep

from schemas.tramite import TramiteRespuesta

from domain.tramite import EstadoTramite

router = APIRouter(prefix="/tramites", tags=["Tramites"])

@router.get("/")
async def listar(service:ServiceDep, estado:EstadoTramite | None=None, 
                 skip: Annotated[int, Query(ge=0)] = 0, 
                 limit: Annotated[int, Query(ge=1, le=100)]=10) -> list[TramiteRespuesta]:
    return [TramiteRespuesta.model_validate(t) for t in await service.listar(estado, skip, limit)]