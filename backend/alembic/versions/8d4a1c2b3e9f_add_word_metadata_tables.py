"""add word metadata tables for difficulty, tags, and inflections

Revision ID: 8d4a1c2b3e9f
Revises: c72b9f6e1a44
Create Date: 2026-07-27 15:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8d4a1c2b3e9f"
down_revision: str | Sequence[str] | None = "c72b9f6e1a44"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("words", sa.Column("difficulty_level", sa.String(length=2), nullable=True))
    op.create_check_constraint(
        "ck_word_difficulty_level",
        "words",
        "difficulty_level IS NULL OR difficulty_level IN ('a1', 'a2', 'b1', 'b2', 'c1', 'c2')",
    )

    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_tags_name"), "tags", ["name"], unique=False)

    op.create_table(
        "word_inflections",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("form_type", sa.String(length=32), nullable=False),
        sa.Column("value", sa.String(length=128), nullable=False),
        sa.Column("notes", sa.String(length=255), nullable=False, server_default=""),
        sa.CheckConstraint(
            "form_type IN ("
            "'plural',"
            "'third_person_singular',"
            "'past_simple',"
            "'past_participle',"
            "'present_participle',"
            "'comparative',"
            "'superlative',"
            "'feminine',"
            "'masculine',"
            "'neuter'"
            ")",
            name="ck_word_inflection_form_type",
        ),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("word_id", "form_type", "value", name="uq_word_inflection_per_word"),
    )
    op.create_index(
        op.f("ix_word_inflections_word_id"), "word_inflections", ["word_id"], unique=False
    )

    op.create_table(
        "word_tags",
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("word_id", "tag_id"),
        sa.UniqueConstraint("word_id", "tag_id", name="uq_word_tag"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("word_tags")
    op.drop_index(op.f("ix_word_inflections_word_id"), table_name="word_inflections")
    op.drop_table("word_inflections")
    op.drop_index(op.f("ix_tags_name"), table_name="tags")
    op.drop_table("tags")
    op.drop_constraint("ck_word_difficulty_level", "words", type_="check")
    op.drop_column("words", "difficulty_level")
