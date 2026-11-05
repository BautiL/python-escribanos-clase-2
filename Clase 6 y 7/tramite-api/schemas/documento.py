from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

class DocumentoCrear(BaseModel):
    nombre: Annotated[str, Field(min_length=5, max_length=50)]
    tipo: Annotated[str, Field(min_length=5, max_length=50)]
    tamanio: Annotated[int|None, Field(ge=0)] = None

class DocumentoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    nombre: str
    tipo: str
    tamanio: int | None = None
    tramite_id: int | None = None