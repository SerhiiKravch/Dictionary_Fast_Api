"""add word senses and example sentences

Revision ID: 6f8e9a0b1c2d
Revises: 1a7b2c3d4e5f
Create Date: 2026-07-27 18:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6f8e9a0b1c2d"
down_revision: str | Sequence[str] | None = "1a7b2c3d4e5f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "word_senses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("part_of_speech", sa.String(length=20), nullable=False),
        sa.Column("primary_translation", sa.String(length=256), nullable=False),
        sa.Column("definition", sa.Text(), nullable=False, server_default=""),
        sa.Column("position", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "position >= 1",
            name="ck_word_sense_position_positive",
        ),
        sa.CheckConstraint(
            "part_of_speech IN ("
            "'noun',"
            "'verb',"
            "'adjective',"
            "'adverb',"
            "'pronoun',"
            "'preposition',"
            "'conjunction',"
            "'interjection',"
            "'phrase',"
            "'other'"
            ")",
            name="ck_word_sense_part_of_speech",
        ),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("word_id", "position", name="uq_word_sense_position"),
    )
    op.create_index(op.f("ix_word_senses_word_id"), "word_senses", ["word_id"], unique=False)

    op.create_table(
        "example_sentences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sense_id", sa.Integer(), nullable=False),
        sa.Column("source_text", sa.Text(), nullable=False),
        sa.Column("translated_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("position", sa.Integer(), nullable=False, server_default="1"),
        sa.CheckConstraint(
            "position >= 1",
            name="ck_example_sentence_position_positive",
        ),
        sa.ForeignKeyConstraint(["sense_id"], ["word_senses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sense_id", "position", name="uq_example_sentence_position"),
    )
    op.create_index(
        op.f("ix_example_sentences_sense_id"),
        "example_sentences",
        ["sense_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_example_sentences_sense_id"), table_name="example_sentences")
    op.drop_table("example_sentences")
    op.drop_index(op.f("ix_word_senses_word_id"), table_name="word_senses")
    op.drop_table("word_senses")
