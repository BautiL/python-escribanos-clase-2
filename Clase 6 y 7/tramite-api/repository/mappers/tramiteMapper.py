from domain.tramite import Tramite
from repository.models.tramiteModel import TramiteModel
from repository.mappers.documentoMapper import DocumentoMapper

class TramiteMapper:
    @staticmethod
    def to_model(tramite: Tramite) -> TramiteModel:
        return TramiteModel(
            id=tramite.id,
            tipo= tramite.tipo,
            cliente= tramite.cliente,
            monto = tramite.monto,
            estado=tramite.estado,
            documentos = [DocumentoMapper.to_model(documento) for documento in tramite.documentos]
        )

    @staticmethod
    def to_domain(tramite_model: TramiteModel) -> Tramite:
        return Tramite(
            id=tramite_model.id,
            tipo= tramite_model.tipo,
            cliente= tramite_model.cliente,
            monto = tramite_model.monto,
            estado=tramite_model.estado,
            documentos = [
                DocumentoMapper.to_domain(documento_model) for documento_model in tramite_model.documentos
            ]
        )