from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.enums import LanguageCode, PartOfSpeech


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
    origin: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    translation_options: Mapped[list["TranslationOption"]] = relationship(
        back_populates="word",
        cascade="all, delete-orphan",
        order_by="TranslationOption.priority",
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
