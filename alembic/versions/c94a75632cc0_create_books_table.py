"""create books table

Revision ID: c94a75632cc0
Revises: 85ba4625b8b3
Create Date: 2026-09-19 15:04:52.033511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c94a75632cc0'
down_revision: Union[str, Sequence[str], None] = '85ba4625b8b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "books" not in inspector.get_table_names():
        op.create_table(
            "books",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("title", sa.String(), nullable=False),
            sa.Column("author", sa.String(), nullable=False),
            sa.Column("description", sa.String(), nullable=True),
            sa.Column("price", sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )

        op.create_index(
            op.f("ix_books_id"),
            "books",
            ["id"],
            unique=False,
        )


def downgrade() -> None:
    op.drop_index(op.f("ix_books_id"), table_name="books")
    op.drop_table("books")