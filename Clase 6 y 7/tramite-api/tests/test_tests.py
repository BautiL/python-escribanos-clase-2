import asyncio
import os
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from dependencies import get_uow
from domain.documento import Documento
from domain.errores import DocumentoNoEncontrado, TramiteFinalizado, TramiteNoEncontrado
from domain.tramite import EstadoTramite, Tramite
from main import app
from repository.database import Base
from repository.documento_repository import RepositorioDocumentoSqlalchemy
from repository.tramite_repository import RepositorioTramiteSqlalchemy
from schemas.documento import DocumentoCrear
from schemas.tramite import TramiteActualizar, TramiteCrear
from service.documento_service import DocumentoService
from service.tramite_service import TramiteService

# Base SEPARADA para tests: el test de integracion hace drop_all y no debe tocar tramites_db
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:admin@localhost:5432/tramites_db_test",
)


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

    async def listar(self, estado=None, skip=0, limit=None):
        items = list(self.items.values())
        if estado is not None:
            items = [i for i in items if i.estado == estado]
        fin = None if limit is None else skip + limit
        return items[skip:fin]

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


@pytest.fixture
def uow():
    return FakeUnitOfWork()


@pytest.fixture
def client(uow):
    app.dependency_overrides[get_uow] = lambda: uow
    try:
        with TestClient(app) as c:
            yield c
    finally:
        app.dependency_overrides.clear()


def _tramite(estado=EstadoTramite.INICIADO, **kwargs):
    datos = {"tipo": "compraventa", "cliente": "Ana Gomez", "monto": 1000.0} | kwargs
    return Tramite(estado=estado, **datos)


# ---------------------------------------------------------------- dominio / schemas

def test_tramite_se_crea_con_estado_iniciado():
    tramite = Tramite(tipo="compraventa", cliente="Ana Gomez", monto=150000)

    assert tramite.estado == EstadoTramite.INICIADO
    assert tramite.documentos == []


def test_validacion_de_monto_de_tramite():
    with pytest.raises(ValueError):
        TramiteCrear.model_validate({"tipo": "compraventa", "cliente": "juan perez", "monto": 0})


# ---------------------------------------------------------------- servicios

def test_tramite_service_guarda_el_tramite(uow):
    async def _ejecutar():
        service = TramiteService(uow)
        tramite = await service.crear(
            TramiteCrear(tipo="compraventa", cliente="pablo gomez", monto=200000)
        )
        assert await uow.tramites.buscar(1) == tramite

    asyncio.run(_ejecutar())


def test_tramite_service_guarda_tramite_mock(uow):
    async def _ejecutar():
        service = TramiteService(uow)

        uow.__aenter__ = AsyncMock(return_value=uow)
        uow.__aexit__ = AsyncMock(return_value=None)
        uow.tramites.guardar = AsyncMock(side_effect=lambda tramite: tramite)

        tramite = await service.crear(TramiteCrear(tipo="compraventa", cliente="pablo perez", monto=50000))

        uow.tramites.guardar.assert_awaited_once()
        assert tramite.tipo == "compraventa"
        assert tramite.cliente == "pablo perez"
        assert tramite.monto == 50000

    asyncio.run(_ejecutar())


def test_tramite_service_no_modifica_finalizado(uow):
    async def _ejecutar():
        await uow.tramites.guardar(_tramite(EstadoTramite.FINALIZADO))
        service = TramiteService(uow)
        with pytest.raises(TramiteFinalizado):
            await service.actualizar(1, TramiteActualizar(monto=5))
        with pytest.raises(TramiteFinalizado):
            await service.eliminar(1)

    asyncio.run(_ejecutar())


def test_tramite_service_obtener_inexistente(uow):
    with pytest.raises(TramiteNoEncontrado):
        asyncio.run(TramiteService(uow).obtener(99))


def test_documento_service_rechaza_documento_de_otro_tramite(uow):
    async def _ejecutar():
        await uow.tramites.guardar(_tramite())
        await uow.tramites.guardar(_tramite())
        await uow.documentos.guardar(Documento(nombre="dni.pdf", tipo="identidad", tramite_id=1))
        service = DocumentoService(uow)
        with pytest.raises(DocumentoNoEncontrado):
            await service.obtener(2, 1)

    asyncio.run(_ejecutar())


# ---------------------------------------------------------------- HTTP

def test_integracion_http(client):
    response = client.post(
        "/tramites/", json={"tipo": "compraventa", "cliente": "sofia lopez", "monto": 32000}
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["tipo"] == "compraventa"
    assert payload["cliente"] == "sofia lopez"
    assert payload["monto"] == 32000
    assert payload["estado"] == "iniciado"


def test_http_crud_tramite(client):
    client.post("/tramites/", json={"tipo": "compraventa", "cliente": "Ana Gomez", "monto": 100})

    assert client.get("/tramites/1").json()["cliente"] == "Ana Gomez"

    r = client.put("/tramites/1", json={"tipo": "alquiler", "cliente": "Ana Gomez", "monto": 200})
    assert r.status_code == 200 and r.json()["tipo"] == "alquiler"

    r = client.patch("/tramites/1", json={"monto": 300})
    assert r.status_code == 200
    assert r.json()["monto"] == 300 and r.json()["tipo"] == "alquiler"

    assert client.delete("/tramites/1").status_code == 204
    assert client.get("/tramites/1").status_code == 404


def test_http_listar_filtra_y_pagina(client, uow):
    async def _cargar():
        await uow.tramites.guardar(_tramite())
        await uow.tramites.guardar(_tramite(EstadoTramite.FINALIZADO))
        await uow.tramites.guardar(_tramite())

    asyncio.run(_cargar())

    assert len(client.get("/tramites/").json()) == 3
    assert [t["id"] for t in client.get("/tramites/?estado=iniciado").json()] == [1, 3]
    assert [t["id"] for t in client.get("/tramites/?skip=1&limit=1").json()] == [2]


def test_http_errores_de_dominio(client, uow):
    asyncio.run(uow.tramites.guardar(_tramite(EstadoTramite.FINALIZADO)))
    documento = {"nombre": "dni.pdf", "tipo": "identidad"}

    assert client.post("/tramites/99/documentos/", json=documento).status_code == 404
    assert client.get("/tramites/99/documentos/").status_code == 404
    assert client.post("/tramites/1/documentos/", json=documento).status_code == 409
    assert client.patch("/tramites/1", json={"monto": 10}).status_code == 409


def test_http_documentos(client):
    client.post("/tramites/", json={"tipo": "compraventa", "cliente": "Ana Gomez", "monto": 100})

    r = client.post("/tramites/1/documentos/", json={"nombre": "dni.pdf", "tipo": "identidad", "tamanio": 10})
    assert r.status_code == 201
    assert r.json() == {"id": 1, "nombre": "dni.pdf", "tipo": "identidad", "tamanio": 10, "tramite_id": 1}

    assert len(client.get("/tramites/1/documentos/").json()) == 1
    assert client.get("/tramites/1/documentos/1").status_code == 200
    assert client.delete("/tramites/1/documentos/1").status_code == 204
    assert client.get("/tramites/1/documentos/1").status_code == 404


# ---------------------------------------------------------------- base de datos real

def test_integracion_bd():
    async def _ejecutar():
        engine = create_async_engine(TEST_DATABASE_URL, echo=False)

        try:
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception:
            await engine.dispose()
            pytest.skip("La base de tests no está disponible (TEST_DATABASE_URL)")

        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

            session_factory = async_sessionmaker(engine, expire_on_commit=False)
            async with session_factory() as session:
                repo = RepositorioTramiteSqlalchemy(session)
                docs = RepositorioDocumentoSqlalchemy(session)

                guardado = await repo.guardar(_tramite(tipo="alquiler", cliente="Pedro Ruiz", monto=300000))
                assert guardado.id is not None

                encontrado = await repo.buscar(guardado.id)
                assert encontrado is not None
                assert encontrado.tipo == "alquiler"
                assert encontrado.estado == EstadoTramite.INICIADO

                # el enum se guarda por valor ("iniciado"), igual que en la migracion
                valor = await session.scalar(text("SELECT estado::text FROM tramites"))
                assert valor == "iniciado"

                # actualizar un tramite existente (antes hacia un INSERT duplicado)
                encontrado.monto = 1
                await repo.guardar(encontrado)
                assert (await repo.buscar(guardado.id)).monto == 1

                # borrar un tramite con documentos (antes fallaba por el NOT NULL)
                await docs.guardar(Documento(nombre="dni.pdf", tipo="identidad", tramite_id=guardado.id))
                session.expunge_all()
                await repo.eliminar(guardado.id)
                assert await docs.listar() == []
                await session.commit()
        finally:
            await engine.dispose()

    asyncio.run(_ejecutar())
