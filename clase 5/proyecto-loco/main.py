from fastapi import FastAPI
from routers import homeRouter

app = FastAPI()
app.include_router(homeRouter.router)