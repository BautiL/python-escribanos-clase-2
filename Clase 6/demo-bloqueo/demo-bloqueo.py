import asyncio
import time

from fastapi import FastAPI

app = FastAPI()

@app.get("/lento-async-mal")
async def lento_async_mal() -> dict[str, str]:
    time.sleep(4) # bloqueo de 4 segundos en un async def
    return {"endpoint": "async con time.sleep"}

@app.get("/lento-sync")
def lento_sync() -> dict[str, str]:
    time.sleep(4) # bloqueo de 4 segundos en un async def
    return {"endpoint": "def con time.sleep"}

@app.get("/lento-async-bien")
async def lento_async_bien() -> dict[str, str]:
    await asyncio.sleep(4) # el loop puede ser atendiendo otros request ("esperando, pero cediendo el turno")
    return {"endpoint": "async con await asyncio.sleep"}

@app.get("/rapido")
async def rapido() -> dict[str, str]:
    return {"endpoint": "rapido"}