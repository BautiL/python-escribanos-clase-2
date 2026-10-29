from fastapi import FastAPI
from routers import tramite_router

app = FastAPI(title="Gestion de tramites")
app.include_router(tramite_router.router)