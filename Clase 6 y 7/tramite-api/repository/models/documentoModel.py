from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from repository.database import Base

if TYPE_CHECKING:
    from repository.models.tramiteModel import TramiteModel

class DocumentoModel(Base):
    __tablename__ = "documentos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str]
    tipo: Mapped[str]
    tamanio: Mapped[int | None] = mapped_column(nullable=True)
    tramite_id: Mapped[int] = mapped_column(ForeignKey("tramites.id"), nullable=False)

    tramite: Mapped["TramiteModel"] = relationship(
    back_populates="documentos", lazy="selectin"
    )       