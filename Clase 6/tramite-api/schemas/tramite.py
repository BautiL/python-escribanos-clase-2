from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field 

from domain.tramite import EstadoTramite

class TramiteCrear(BaseModel): 
    """Lo que manda el cliente para crear (POST) o reemplazar (PUT) un tramite."""
    # Annotated[tipo, reglas]
    tipo: Annotated[str, Field(min_length=3, max_length=50, examples=["compraventa"])]
    cliente: Annotated[str, Field(min_length=3, examples=["Ana Gomez"])]
    monto: Annotated[float, Field(gt=0, examples=[150000])] # gt = greater than (> 0)

class TramiteActualizar(BaseModel): 
    """Patch: el cliente manda solo lo que quiere cambiar, asi que todo es opcional!!!"""
    tipo: Annotated[str | None, Field(min_length=3, max_length=50, examples=["compraventa"])] = None
    cliente: Annotated[str | None, Field(min_length=3, examples=["Ana Gomez"])] = None
    monto: Annotated[float | None, Field(gt=0, examples=[150000])] = None

class TramiteRespuesta(BaseModel):
    """Lo que devuelve la API."""
    # "podes armarme a partir de cualquier objeto que tengas estos atributos (por ejemplo, del dataclass Tramite del dominio)"
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: str
    cliente: str
    monto: float
    estado: EstadoTramite