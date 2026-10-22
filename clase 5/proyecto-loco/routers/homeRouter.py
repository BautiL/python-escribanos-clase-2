from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from service.homeService import HomeService

class Item(BaseModel):
    nombre: str
    precio: float | None = 100
    disponible: bool

def get_service():
    return HomeService()

router = APIRouter(prefix='/home')


@router.get('/')
async def root():
    return {"mensaje":"hola mundo!"}

@router.get('/getTexto')
async def obtener_texto(service: HomeService = Depends(get_service)):  # noqa: B008
    return service.get_texto_home()

@router.get('/obtenerNumero/{numero}')
async def obtenerNumero(numero: int):
    return numero

@router.get('/sumar')
async def suma(numero1:int, numero2:int, req:Request):
    return str(numero1) + str(numero2) + str(req.query_params)

@router.post('/item')
async def mandar_item(item: Item):
    return item