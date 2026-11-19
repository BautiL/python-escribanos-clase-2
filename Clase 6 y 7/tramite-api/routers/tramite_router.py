from typing import Annotated

from fastapi import APIRouter, Query, status

from dependencies import ServiceDep
from domain.tramite import EstadoTramite
from schemas.tramite import TramiteActualizar, TramiteCrear, TramiteRespuesta

router = APIRouter(prefix="/tramites", tags=["Tramites"])


@router.get("/")
async def listar(
    service: ServiceDep,
    estado: EstadoTramite | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> list[TramiteRespuesta]:
    return [TramiteRespuesta.model_validate(t) for t in await service.listar(estado, skip, limit)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear(datos: TramiteCrear, service: ServiceDep) -> TramiteRespuesta:
    tramite = await service.crear(datos)
    return TramiteRespuesta.model_validate(tramite)


@router.get("/{tramite_id}")
async def obtener(tramite_id: int, service: ServiceDep) -> TramiteRespuesta:
    return TramiteRespuesta.model_validate(await service.obtener(tramite_id))


@router.put("/{tramite_id}")
async def reemplazar(tramite_id: int, datos: TramiteCrear, service: ServiceDep) -> TramiteRespuesta:
    return TramiteRespuesta.model_validate(await service.reemplazar(tramite_id, datos))


@router.patch("/{tramite_id}")
async def actualizar(
    tramite_id: int, datos: TramiteActualizar, service: ServiceDep
) -> TramiteRespuesta:
    return TramiteRespuesta.model_validate(await service.actualizar(tramite_id, datos))


@router.delete("/{tramite_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar(tramite_id: int, service: ServiceDep) -> None:
    await service.eliminar(tramite_id)
