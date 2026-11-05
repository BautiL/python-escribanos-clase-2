from domain.documento import Documento
from repository.models.documentoModel import DocumentoModel

class DocumentoMapper:
    @staticmethod
    def to_model(documento: Documento) -> DocumentoModel:
        return DocumentoModel(
            id= documento.id,
            nombre = documento.nombre,
            tipo = documento.tipo,
            tamanio = documento.tamanio,
            tramite_id = documento.tramite_id
        )

    @staticmethod
    def to_domain(documento_model: DocumentoModel) -> Documento:
        return Documento(
            id= documento_model.id,
            nombre = documento_model.nombre,
            tipo = documento_model.tipo,
            tamanio = documento_model.tamanio,
            tramite_id = documento_model.tramite_id,
            tramite = getattr(documento_model, "tramite", None)
        )