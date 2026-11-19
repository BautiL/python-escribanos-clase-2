from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioCrear(BaseModel):
    email: EmailStr
    nombre: Annotated[str, Field(min_length=3, max_length=100, examples=["Ana Gomez"])]
    password: Annotated[str, Field(min_length=8, max_length=128)]


class UsuarioRespuesta(BaseModel):
    """Sin password_hash: lo que no está en el schema no sale en la respuesta."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    nombre: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"