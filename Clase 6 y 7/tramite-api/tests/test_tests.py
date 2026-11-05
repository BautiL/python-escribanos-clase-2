import asyncio

import pytest

from domain.documento import Documento
from domain.errores import TramiteFinalizado, TramiteNoEncontrado
from domain.tramite import Tramite, EstadoTramite
from schemas.documento import DocumentoCrear
from schemas.tramite import TramiteCrear
from service.documento_service import DocumentoService
from service.tramite_service import TramiteService

class FakeRepositorio:
    def __init__(self, items=None):
        self.items = items or {}

    async def guardar(self, entidad):
        if entidad.id is None:
            entidad.id = max(self.items.keys(), default=0) + 1
        self.items[entidad.id] = entidad
        return entidad

    async def buscar(self, entidad_id):
        return self.items.get(entidad_id)

    async def listar(self):
        return list(self.items.values())

    async def listar_por_tramite(self, tramite_id):
        return [doc for doc in self.items.values() if getattr(doc, "tramite_id", None) == tramite_id]

    async def eliminar(self, entidad_id):
        self.items.pop(entidad_id, None)

class FakeUnitOfWork:
    def __init__(self, tramites=None, documentos=None):
        self.tramites = tramites or FakeRepositorio()
        self.documentos = documentos or FakeRepositorio()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return None

    async def commit(self):
        return None

    async def rollback(self):
        return None

def test_tramite_se_crea_con_estado_iniciado():
    tramite = Tramite(tipo="compraventa", cliente="Ana Gomez", monto=150000)

    assert tramite.estado == EstadoTramite.INICIADO
    assert tramite.documentos == []

def test_validacion_de_monto_de_tramite():
    with pytest.raises(ValueError):
        TramiteCrear.model_validate(
            {
                "tipo": "compraventa",
                "cliente": "juan perez",
                "monto": 0,
            }
        )

def test_tramite_service_guarda_el_tramite():
    async def _ejecutar():
        uow = FakeUnitOfWork()
        service = TramiteService(uow)

        tramite = await service.crear(
            TramiteCrear(tipo="compraventa", cliente="pablo gomez", monto=200000)
        )

        assert await uow.tramites.buscar(1) == tramite

    asyncio.run(_ejecutar())