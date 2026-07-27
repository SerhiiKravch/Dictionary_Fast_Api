from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.enums import InflectionType, LanguageCode, PartOfSpeech, WordOrigin

word_tags = Table(
    "word_tags",
    Base.metadata,
    Column("word_id", ForeignKey("words.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("word_id", "tag_id", name="uq_word_tag"),
)


class Word(Base):
    __tablename__ = "words"
    __table_args__ = (
        UniqueConstraint(
            "source_word",
            "source_language",
            "target_language",
            name="uq_word_direction",
        ),
        UniqueConstraint("slug", name="uq_word_slug"),
        CheckConstraint(
            "source_language <> target_language",
            name="ck_word_different_languages",
        ),
        CheckConstraint(
            "origin IN ('manual', 'openai', 'imported')",
            name="ck_word_origin",
        ),
        CheckConstraint(
            "difficulty_level IS NULL OR difficulty_level IN ('a1', 'a2', 'b1', 'b2', 'c1', 'c2')",
            name="ck_word_difficulty_level",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_word: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    source_language: Mapped[str] = mapped_column(
        String(2), default=LanguageCode.ENGLISH.value, nullable=False
    )
    target_language: Mapped[str] = mapped_column(
        String(2), default=LanguageCode.UKRAINIAN.value, nullable=False
    )
    slug: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    transcription: Mapped[str] = mapped_column(String(128), nullable=False)
    primary_translation: Mapped[str] = mapped_column(String(256), nullable=False)
    context_sentence: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty_level: Mapped[str | None] = mapped_column(String(2), nullable=True)
    origin: Mapped[str] = mapped_column(
        String(20),
        default=WordOrigin.MANUAL.value,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    translation_options: Mapped[list["TranslationOption"]] = relationship(
        back_populates="word",
        cascade="all, delete-orphan",
        order_by="TranslationOption.priority",
    )
    inflections: Mapped[list["WordInflection"]] = relationship(
        back_populates="word",
        cascade="all, delete-orphan",
        order_by="WordInflection.id",
    )
    tags: Mapped[list["Tag"]] = relationship(
        secondary=word_tags,
        back_populates="words",
        order_by="Tag.name",
    )


class TranslationOption(Base):
    __tablename__ = "translation_options"
    __table_args__ = (
        UniqueConstraint(
            "word_id",
            "text",
            "part_of_speech",
            name="uq_translation_option_per_word",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), index=True, nullable=False
    )
    text: Mapped[str] = mapped_column(String(256), nullable=False)
    part_of_speech: Mapped[str] = mapped_column(
        String(20), default=PartOfSpeech.OTHER.value, nullable=False
    )
    priority: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    usage_note: Mapped[str] = mapped_column(String(255), default="", nullable=False)

    word: Mapped["Word"] = relationship(back_populates="translation_options")


class WordInflection(Base):
    __tablename__ = "word_inflections"
    __table_args__ = (
        CheckConstraint(
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
        UniqueConstraint(
            "word_id",
            "form_type",
            "value",
            name="uq_word_inflection_per_word",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), index=True, nullable=False
    )
    form_type: Mapped[str] = mapped_column(
        String(32), default=InflectionType.PLURAL.value, nullable=False
    )
    value: Mapped[str] = mapped_column(String(128), nullable=False)
    notes: Mapped[str] = mapped_column(String(255), default="", nullable=False)

    word: Mapped["Word"] = relationship(back_populates="inflections")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)

    words: Mapped[list[Word]] = relationship(
        secondary=word_tags,
        back_populates="tags",
    )
