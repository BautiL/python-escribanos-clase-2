from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependencies import DocumentoServiceDep
from schemas.documento import DocumentoCrear, DocumentoRespuesta

router = APIRouter(prefix="/tramites/{tramite_id}/documentos", tags=["Documentos"])


@router.get("/", response_model=list[DocumentoRespuesta])
async def listar_documentos(
    tramite_id: int,
    service: DocumentoServiceDep,
):
    return [DocumentoRespuesta.model_validate(d) for d in await service.listar_por_tramite(tramite_id)]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DocumentoRespuesta)
async def crear_documento(
    tramite_id: int,
    datos: DocumentoCrear,
    service: DocumentoServiceDep,
):
    documento = await service.crear(tramite_id, datos)
    return DocumentoRespuesta.model_validate(documento)
