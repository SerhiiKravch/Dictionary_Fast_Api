from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.database import DatabaseIntegrityError
from app.exceptions.dictionary import EmptyWordError, InvalidDirectionError
from app.models.enums import LanguageCode
from app.models.word import TranslationOption, Word
from app.schemas.word import GeneratedWordPayload


def normalize_word(word: str) -> str:
    normalized = word.strip().lower()
    if not normalized:
        raise EmptyWordError("Word cannot be empty.")
    return normalized


def parse_direction(direction: str) -> tuple[LanguageCode, LanguageCode]:
    try:
        source, target = direction.split(":")
        return LanguageCode(source), LanguageCode(target)
    except ValueError as exc:
        raise InvalidDirectionError("Invalid direction format. Expected 'en:uk'.") from exc


def get_existing_word(
    db: Session,
    word: str,
    source_language: LanguageCode,
    target_language: LanguageCode,
) -> Word | None:
    stmt = select(Word).where(
        Word.source_word == normalize_word(word),
        Word.source_language == source_language.value,
        Word.target_language == target_language.value,
    )
    return db.execute(stmt).scalar_one_or_none()


def create_word_with_options(
    db: Session,
    payload: GeneratedWordPayload,
    slug: str,
) -> Word:
    try:
        word = Word(
            source_word=normalize_word(payload.source_word),
            source_language=payload.source_language.value,
            target_language=payload.target_language.value,
            slug=slug,
            transcription=payload.transcription,
            primary_translation=payload.primary_translation,
            context_sentence=payload.context_sentence,
            origin=payload.origin,
        )
        db.add(word)
        db.flush()

        for option in payload.translation_options:
            db.add(
                TranslationOption(
                    word_id=word.id,
                    text=option.text,
                    part_of_speech=option.part_of_speech.value,
                    priority=option.priority,
                    usage_note=option.usage_note,
                )
            )

        db.commit()
        db.refresh(word)
        return word

    except IntegrityError as exc:
        db.rollback()
        raise DatabaseIntegrityError("Failed to save word due to DB constraint.") from exc
