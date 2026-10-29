from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from repository.database import Base

from domain.tramite import EstadoTramite

class TramiteModel(Base):
    __tablename__ = "tramites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tipo: Mapped[str]
    cliente: Mapped[str]
    monto: Mapped[float]
    estado: Mapped[EstadoTramite] = mapped_column(SQLEnum(EstadoTramite, name="estado_tramite", create_type=True),
                                                default=EstadoTramite.INICIADO, nullable=False)