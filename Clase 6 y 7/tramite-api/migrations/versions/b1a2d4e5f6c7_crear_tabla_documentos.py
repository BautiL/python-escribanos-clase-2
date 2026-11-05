"""crear tabla documentos

Revision ID: b1a2d4e5f6c7
Revises: cf6ff646ccb1
Create Date: 2026-11-05 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b1a2d4e5f6c7"
down_revision: Union[str, Sequence[str], None] = "cf6ff646ccb1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "documentos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("tipo", sa.String(), nullable=False),
        sa.Column("tamaño", sa.Integer(), nullable=True),
        sa.Column("tramite_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["tramite_id"], ["tramites.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("documentos")
