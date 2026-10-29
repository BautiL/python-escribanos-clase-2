from domain.tramite import Tramite
from repository.models.tramiteModel import TramiteModel

class TramiteMapper:
    @staticmethod
    def to_model(tramite: Tramite) -> TramiteModel:
        return TramiteModel(
            id=tramite.id,
            tipo= tramite.tipo,
            cliente= tramite.cliente,
            monto = tramite.monto,
            estado=tramite.estado
        )

    @staticmethod
    def to_domain(tramite_model: TramiteModel) -> Tramite:
        return Tramite(
            id=tramite_model.id,
            tipo= tramite_model.tipo,
            cliente= tramite_model.cliente,
            monto = tramite_model.monto,
            estado=tramite_model.estado
        )