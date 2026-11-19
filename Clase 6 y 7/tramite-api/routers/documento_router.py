from fastapi import APIRouter, status

from dependencies import DocumentoServiceDep
from schemas.documento import DocumentoCrear, DocumentoRespuesta

router = APIRouter(prefix="/tramites/{tramite_id}/documentos", tags=["Documentos"])


@router.get("/")
async def listar_documentos(
    tramite_id: int, service: DocumentoServiceDep
) -> list[DocumentoRespuesta]:
    return [
        DocumentoRespuesta.model_validate(d) for d in await service.listar_por_tramite(tramite_id)
    ]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_documento(
    tramite_id: int, datos: DocumentoCrear, service: DocumentoServiceDep
) -> DocumentoRespuesta:
    documento = await service.crear(tramite_id, datos)
    return DocumentoRespuesta.model_validate(documento)


@router.get("/{documento_id}")
async def obtener_documento(
    tramite_id: int, documento_id: int, service: DocumentoServiceDep
) -> DocumentoRespuesta:
    return DocumentoRespuesta.model_validate(await service.obtener(tramite_id, documento_id))


@router.delete("/{documento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_documento(
    tramite_id: int, documento_id: int, service: DocumentoServiceDep
) -> None:
    await service.eliminar(tramite_id, documento_id)
