"""add word constraints, origin enum semantics, and updated_at

Revision ID: c72b9f6e1a44
Revises: 4629186736bf
Create Date: 2026-07-20 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c72b9f6e1a44"
down_revision: str | Sequence[str] | None = "4629186736bf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove legacy rows that violate the new direction rule.
    op.execute(
        sa.text(
            """
            DELETE FROM words
            WHERE source_language = target_language
            """
        )
    )
    # Normalize free-form origin values before constraining them.
    op.execute(
        sa.text(
            """
            UPDATE words
            SET origin = CASE
                WHEN lower(trim(origin)) IN ('manual', 'openai', 'imported')
                    THEN lower(trim(origin))
                WHEN origin IS NULL OR trim(origin) = ''
                    THEN 'manual'
                ELSE 'manual'
            END
            """
        )
    )

    op.alter_column(
        "words",
        "origin",
        existing_type=sa.Text(),
        type_=sa.String(length=20),
        existing_nullable=False,
    )
    op.add_column(
        "words",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_check_constraint(
        "ck_word_different_languages",
        "words",
        "source_language <> target_language",
    )
    op.create_check_constraint(
        "ck_word_origin",
        "words",
        "origin IN ('manual', 'openai', 'imported')",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("ck_word_origin", "words", type_="check")
    op.drop_constraint("ck_word_different_languages", "words", type_="check")
    op.drop_column("words", "updated_at")
    op.alter_column(
        "words",
        "origin",
        existing_type=sa.String(length=20),
        type_=sa.Text(),
        existing_nullable=False,
    )
