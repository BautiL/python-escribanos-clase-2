from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.tramite import EstadoTramite
from repository.database import Base

if TYPE_CHECKING:
    from repository.models.documentoModel import DocumentoModel


class TramiteModel(Base):
    __tablename__ = "tramites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tipo: Mapped[str]
    cliente: Mapped[str]
    monto: Mapped[float]
    # values_callable: guarda el VALOR del enum ("iniciado") y no el NOMBRE ("INICIADO"),
    # que es lo que espera el tipo estado_tramite creado por la migracion.
    estado: Mapped[EstadoTramite] = mapped_column(
        SQLEnum(
            EstadoTramite,
            name="estado_tramite",
            create_type=True,
            values_callable=lambda enum: [miembro.value for miembro in enum],
        ),
        default=EstadoTramite.INICIADO,
        nullable=False,
    )
    # cascade: al borrar un tramite se borran sus documentos
    # (sin esto SQLAlchemy intenta poner tramite_id = NULL y falla por el NOT NULL).
    documentos: Mapped[list["DocumentoModel"]] = relationship(
        back_populates="tramite",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
