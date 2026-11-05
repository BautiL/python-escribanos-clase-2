# init_db.py
import asyncio

from repository.database import Base, engine
# ⚠️ IMPORTANTE: Importar los modelos
import repository.models.tramiteModel
import repository.models.documentoModel


async def init_db():
    async with engine.begin() as conn:
        print("Creando tablas en PostgreSQL...")
        await conn.run_sync(Base.metadata.create_all)
        print("¡Tablas creadas con éxito!")


if __name__ == "__main__":
    asyncio.run(init_db())