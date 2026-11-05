from fastapi import FastAPI

from routers import documento_router, tramite_router

app = FastAPI(title="Gestion de tramites", debug=True)
app.include_router(tramite_router.router)
app.include_router(documento_router.router)