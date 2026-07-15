from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.exceptions.database import DatabaseIntegrityError
from app.exceptions.dictionary import (
    EmptyWordError,
    InvalidDirectionError,
    SameLanguageDirectionError,
    WordAlreadyExistsError,
    WordNotFoundError,
)
from app.models.enums import LanguageCode
from app.models.word import TranslationOption, Word
from app.schemas.word import GeneratedWordPayload, WordCreate, WordLookupRequest
from app.services.openai_service import OpenAIService
from app.utils.slug import build_base_slug, build_slug_with_suffix, generate_slug_suffix


def normalize_word(word: str) -> str:
    normalized = word.strip().lower()
    if not normalized:
        raise EmptyWordError("Word cannot be empty.")
    return normalized


def validate_language_direction(
    source_language: LanguageCode,
    target_language: LanguageCode,
) -> None:
    if source_language == target_language:
        raise SameLanguageDirectionError("Source and target languages must be different.")


def parse_direction(direction: str) -> tuple[LanguageCode, LanguageCode]:
    try:
        source, target = direction.split(":")
        source_language = LanguageCode(source)
        target_language = LanguageCode(target)
        validate_language_direction(source_language, target_language)
        return source_language, target_language
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


def get_word_by_slug(db: Session, slug: str) -> Word:
    stmt = select(Word).where(Word.slug == slug)
    word = db.execute(stmt).scalar_one_or_none()

    if word is None:
        raise WordNotFoundError(f"Word with slug '{slug}' not found.")

    return word


def get_constraint_name(exc: IntegrityError) -> str | None:
    diag = getattr(getattr(exc, "orig", None), "diag", None)
    return getattr(diag, "constraint_name", None)


def persist_word_with_options(
    db: Session,
    *,
    source_word: str,
    source_language: LanguageCode,
    target_language: LanguageCode,
    transcription: str,
    primary_translation: str,
    context_sentence: str,
    origin: str,
    translation_options: list,
) -> Word:
    base_slug = build_base_slug(
        source_word=source_word,
        source_language=source_language,
        target_language=target_language,
    )

    for attempt in range(5):
        slug = build_slug_with_suffix(
            base_slug,
            None if attempt == 0 else generate_slug_suffix(),
        )

        try:
            word = Word(
                source_word=normalize_word(source_word),
                source_language=source_language.value,
                target_language=target_language.value,
                slug=slug,
                transcription=transcription,
                primary_translation=primary_translation,
                context_sentence=context_sentence,
                origin=origin,
            )
            db.add(word)
            db.flush()

            for option in translation_options:
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
            constraint_name = get_constraint_name(exc)

            if constraint_name == "uq_word_direction":
                raise WordAlreadyExistsError(
                    "Word already exists for the selected translation direction."
                ) from exc

            if constraint_name == "uq_word_slug" and attempt < 4:
                continue

            raise DatabaseIntegrityError("Failed to save word due to DB constraint.") from exc

    raise DatabaseIntegrityError("Failed to generate a unique slug for the word.")


def create_word_with_options(
    db: Session,
    payload: GeneratedWordPayload,
) -> Word:
    validate_language_direction(
        payload.source_language,
        payload.target_language,
    )

    return persist_word_with_options(
        db=db,
        source_word=payload.source_word,
        source_language=payload.source_language,
        target_language=payload.target_language,
        transcription=payload.transcription,
        primary_translation=payload.primary_translation,
        context_sentence=payload.context_sentence,
        origin=payload.origin,
        translation_options=payload.translation_options,
    )


def create_word_manually(db: Session, payload: WordCreate) -> Word:
    normalized_word = normalize_word(payload.source_word)
    validate_language_direction(
        payload.source_language,
        payload.target_language,
    )

    existing_word = get_existing_word(
        db=db,
        word=normalized_word,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
    if existing_word is not None:
        raise WordAlreadyExistsError("Word already exists for the selected translation direction.")

    return persist_word_with_options(
        db=db,
        source_word=normalized_word,
        source_language=payload.source_language,
        target_language=payload.target_language,
        transcription=payload.transcription,
        primary_translation=payload.primary_translation,
        context_sentence=payload.context_sentence,
        origin=payload.origin,
        translation_options=payload.translation_options,
    )


def autocomplete_words(db: Session, query: str) -> list[str]:
    normalized = query.strip().lower()
    if not normalized:
        return []

    stmt = (
        select(Word.source_word)
        .where(Word.source_word.ilike(f"{normalized}%"))
        .order_by(Word.source_word.asc())
        .limit(10)
    )

    return list(db.execute(stmt).scalars().all())


def list_words(db: Session) -> list[Word]:
    stmt = (
        select(Word)
        .options(selectinload(Word.translation_options))
        .order_by(Word.created_at.desc())
    )
    return list(db.execute(stmt).scalars().all())


def lookup_or_create_word(db: Session, payload: WordLookupRequest) -> Word:
    normalized_word = normalize_word(payload.word)
    source_language, target_language = parse_direction(payload.direction)

    existing_word = get_existing_word(
        db=db,
        word=normalized_word,
        source_language=source_language,
        target_language=target_language,
    )
    if existing_word is not None:
        return existing_word

    openai_service = OpenAIService()
    generated_payload = openai_service.generate_word_payload(
        word=normalized_word,
        source_language=source_language,
        target_language=target_language,
    )

    return create_word_with_options(
        db=db,
        payload=generated_payload,
    )
