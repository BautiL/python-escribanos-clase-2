from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from repository.database import Base

from domain.tramite import EstadoTramite

if TYPE_CHECKING:
    from repository.models.documentoModel import DocumentoModel

class TramiteModel(Base):
    __tablename__ = "tramites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tipo: Mapped[str]
    cliente: Mapped[str]
    monto: Mapped[float]
    estado: Mapped[EstadoTramite] = mapped_column(SQLEnum(EstadoTramite, name="estado_tramite", create_type=True),
                                                default=EstadoTramite.INICIADO, nullable=False)
    documentos: Mapped[list["DocumentoModel"]] = relationship(
    back_populates="tramite", lazy="selectin"
    )