"""add word relations

Revision ID: 1a7b2c3d4e5f
Revises: 8d4a1c2b3e9f
Create Date: 2026-07-27 17:10:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1a7b2c3d4e5f"
down_revision: str | Sequence[str] | None = "8d4a1c2b3e9f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "word_relations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_word_id", sa.Integer(), nullable=False),
        sa.Column("target_word_id", sa.Integer(), nullable=False),
        sa.Column("relation_type", sa.String(length=20), nullable=False),
        sa.Column("notes", sa.String(length=255), nullable=False, server_default=""),
        sa.CheckConstraint(
            "relation_type IN ('synonym', 'antonym', 'related')",
            name="ck_word_relation_type",
        ),
        sa.CheckConstraint(
            "source_word_id <> target_word_id",
            name="ck_word_relation_not_self",
        ),
        sa.ForeignKeyConstraint(["source_word_id"], ["words.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_word_id"], ["words.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "source_word_id",
            "target_word_id",
            "relation_type",
            name="uq_word_relation_unique",
        ),
    )
    op.create_index(
        op.f("ix_word_relations_source_word_id"),
        "word_relations",
        ["source_word_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_word_relations_target_word_id"),
        "word_relations",
        ["target_word_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_word_relations_target_word_id"), table_name="word_relations")
    op.drop_index(op.f("ix_word_relations_source_word_id"), table_name="word_relations")
    op.drop_table("word_relations")
