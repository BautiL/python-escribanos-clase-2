"""renombrar columna tamaño a tamanio

La migracion anterior creo la columna como "tamaño", pero el modelo
DocumentoModel la mapea como "tamanio".

Revision ID: d4e5f6a7b8c9
Revises: b1a2d4e5f6c7
Create Date: 2026-11-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, Sequence[str], None] = "b1a2d4e5f6c7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("documentos", "tamaño", new_column_name="tamanio")


def downgrade() -> None:
    op.alter_column("documentos", "tamanio", new_column_name="tamaño")
