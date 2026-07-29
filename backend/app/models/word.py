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
from app.models.enums import InflectionType, LanguageCode, PartOfSpeech, RelationType, WordOrigin

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
    outgoing_relations: Mapped[list["WordRelation"]] = relationship(
        back_populates="source_word_ref",
        cascade="all, delete-orphan",
        foreign_keys="WordRelation.source_word_id",
    )
    incoming_relations: Mapped[list["WordRelation"]] = relationship(
        back_populates="target_word_ref",
        cascade="all, delete-orphan",
        foreign_keys="WordRelation.target_word_id",
    )
    senses: Mapped[list["WordSense"]] = relationship(
        back_populates="word",
        cascade="all, delete-orphan",
        order_by="WordSense.position",
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


class WordRelation(Base):
    __tablename__ = "word_relations"
    __table_args__ = (
        CheckConstraint(
            "relation_type IN ('synonym', 'antonym', 'related')",
            name="ck_word_relation_type",
        ),
        CheckConstraint(
            "source_word_id <> target_word_id",
            name="ck_word_relation_not_self",
        ),
        UniqueConstraint(
            "source_word_id",
            "target_word_id",
            "relation_type",
            name="uq_word_relation_unique",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), index=True, nullable=False
    )
    target_word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), index=True, nullable=False
    )
    relation_type: Mapped[str] = mapped_column(
        String(20), default=RelationType.RELATED.value, nullable=False
    )
    notes: Mapped[str] = mapped_column(String(255), default="", nullable=False)

    source_word_ref: Mapped[Word] = relationship(
        back_populates="outgoing_relations",
        foreign_keys=[source_word_id],
    )
    target_word_ref: Mapped[Word] = relationship(
        back_populates="incoming_relations",
        foreign_keys=[target_word_id],
    )


class WordSense(Base):
    __tablename__ = "word_senses"
    __table_args__ = (
        CheckConstraint("position >= 1", name="ck_word_sense_position_positive"),
        CheckConstraint(
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
        UniqueConstraint("word_id", "position", name="uq_word_sense_position"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), index=True, nullable=False
    )
    part_of_speech: Mapped[str] = mapped_column(
        String(20), default=PartOfSpeech.OTHER.value, nullable=False
    )
    primary_translation: Mapped[str] = mapped_column(String(256), nullable=False)
    definition: Mapped[str] = mapped_column(Text, default="", nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    word: Mapped[Word] = relationship(back_populates="senses")
    example_sentences: Mapped[list["ExampleSentence"]] = relationship(
        back_populates="sense",
        cascade="all, delete-orphan",
        order_by="ExampleSentence.position",
    )


class ExampleSentence(Base):
    __tablename__ = "example_sentences"
    __table_args__ = (
        CheckConstraint("position >= 1", name="ck_example_sentence_position_positive"),
        UniqueConstraint("sense_id", "position", name="uq_example_sentence_position"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sense_id: Mapped[int] = mapped_column(
        ForeignKey("word_senses.id", ondelete="CASCADE"), index=True, nullable=False
    )
    source_text: Mapped[str] = mapped_column(Text, nullable=False)
    translated_text: Mapped[str] = mapped_column(Text, default="", nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    sense: Mapped[WordSense] = relationship(back_populates="example_sentences")
