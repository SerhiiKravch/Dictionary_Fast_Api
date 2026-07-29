"""backfill word senses and example sentences from legacy word fields

Revision ID: 7b9c0d1e2f3a
Revises: 6f8e9a0b1c2d
Create Date: 2026-07-29 11:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7b9c0d1e2f3a"
down_revision: str | Sequence[str] | None = "6f8e9a0b1c2d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        sa.text(
            """
            INSERT INTO word_senses (
                word_id,
                part_of_speech,
                primary_translation,
                definition,
                position,
                created_at,
                updated_at
            )
            SELECT
                words.id,
                COALESCE(
                    (
                        SELECT translation_options.part_of_speech
                        FROM translation_options
                        WHERE translation_options.word_id = words.id
                        ORDER BY translation_options.priority ASC, translation_options.id ASC
                        LIMIT 1
                    ),
                    'other'
                ) AS part_of_speech,
                words.primary_translation,
                '' AS definition,
                1 AS position,
                words.created_at,
                words.updated_at
            FROM words
            """
        )
    )

    op.execute(
        sa.text(
            """
            INSERT INTO example_sentences (
                sense_id,
                source_text,
                translated_text,
                position
            )
            SELECT
                word_senses.id,
                words.context_sentence,
                '' AS translated_text,
                1 AS position
            FROM word_senses
            INNER JOIN words ON words.id = word_senses.word_id
            WHERE word_senses.position = 1
            """
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sa.text("DELETE FROM example_sentences"))
    op.execute(sa.text("DELETE FROM word_senses"))
