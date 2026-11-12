import asyncio
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from dependencies import get_uow
from domain.documento import Documento
from domain.errores import TramiteFinalizado, TramiteNoEncontrado
from domain.tramite import Tramite, EstadoTramite
from main import app
from repository.database import Base
from repository.tramite_repository import RepositorioTramiteSqlalchemy
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

def test_tramite_service_guarda_tramite_mock():
    async def _ejecutar():
        uow = FakeUnitOfWork()
        service = TramiteService(uow)

        uow.__aenter__ = AsyncMock(return_value=uow)
        uow.__aexit__ =  AsyncMock(return_value=None)
        uow.tramites.guardar = AsyncMock(side_effect = lambda tramite: tramite)

        tramite = await service.crear(TramiteCrear(tipo="compraventa", cliente="pablo perez", monto=50000))

        uow.tramites.guardar.assert_awaited_once()
        assert tramite.tipo == "compraventa"
        assert tramite.cliente == "pablo perez"
        assert tramite.monto == 50000

    asyncio.run(_ejecutar())

def test_integracion_http():
    uow = FakeUnitOfWork()
    app.dependency_overrides[get_uow] = lambda:uow

    try:
        with TestClient(app) as client:
            response = client.post(
                "/tramites/",
                json={
                    "tipo": "compraventa",
                    "cliente": "sofia lopez",
                    "monto": 32000
                }
            )
        
        assert response.status_code == 201
        payload = response.json()
        assert payload["tipo"] == "compraventa"
        assert payload["cliente"] == "sofia lopez"
        assert payload["monto"] == 32000
        assert payload["estado"] == "iniciado"

    finally:
        app.dependency_overrides.clear()

def test_integracion_bd():
    async def _ejecutar():
        db_url = "postgresql+asyncpg://postgres:admin@localhost:5432/tramite_db"

        engine = create_async_engine(db_url, echo=False)

        try:
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception:
            await engine.dispose()
            pytest.skip("PostgreSQL no está disponible en localhost:5432")

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        async with session_factory() as session:
            repo = RepositorioTramiteSqlalchemy(session)
            tramite = Tramite(tipo="alquiler", cliente="Pedro Ruiz", monto=300000)

            guardado = await repo.guardar(tramite)
            assert guardado.id is not None

            encontrado = await repo.buscar(guardado.id)
            assert encontrado is not None
            assert encontrado.tipo == "alquiler"
            assert encontrado.cliente == "Pedro Ruiz"
            assert encontrado.monto == 300000
            assert encontrado.estado == EstadoTramite.INICIADO

        await engine.dispose()

    asyncio.run(_ejecutar())