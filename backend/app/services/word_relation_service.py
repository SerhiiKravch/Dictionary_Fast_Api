from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, selectinload

from app.exceptions.database import DatabaseConnectionError
from app.exceptions.dictionary import (
    InvalidWordRelationError,
    WordNotFoundError,
    WordRelationAlreadyExistsError,
)
from app.models.enums import RelationType
from app.models.word import Word, WordRelation
from app.schemas.word import WordRelationCreate


def get_word_by_id(db: Session, word_id: int) -> Word:
    try:
        word = db.execute(select(Word).where(Word.id == word_id)).scalar_one_or_none()
    except OperationalError as exc:
        raise DatabaseConnectionError("Database connection failed during word lookup.") from exc

    if word is None:
        raise WordNotFoundError(f"Word with id '{word_id}' not found.")

    return word


def relation_exists(
    db: Session,
    *,
    source_word_id: int,
    target_word_id: int,
    relation_type: RelationType,
) -> bool:
    stmt = select(WordRelation.id).where(
        WordRelation.source_word_id == source_word_id,
        WordRelation.target_word_id == target_word_id,
        WordRelation.relation_type == relation_type.value,
    )
    return db.execute(stmt).scalar_one_or_none() is not None


def build_relation(
    *,
    source_word_id: int,
    target_word_id: int,
    relation_type: RelationType,
    notes: str,
) -> WordRelation:
    return WordRelation(
        source_word_id=source_word_id,
        target_word_id=target_word_id,
        relation_type=relation_type.value,
        notes=notes,
    )


def create_word_relation(db: Session, word_id: int, payload: WordRelationCreate) -> WordRelation:
    source_word = get_word_by_id(db, word_id)
    target_word = get_word_by_id(db, payload.target_word_id)

    if source_word.id == target_word.id:
        raise InvalidWordRelationError("A word cannot be related to itself.")

    if relation_exists(
        db,
        source_word_id=source_word.id,
        target_word_id=target_word.id,
        relation_type=payload.relation_type,
    ):
        raise WordRelationAlreadyExistsError("The selected word relation already exists.")

    if payload.relation_type == RelationType.SYNONYM and relation_exists(
        db,
        source_word_id=target_word.id,
        target_word_id=source_word.id,
        relation_type=payload.relation_type,
    ):
        raise WordRelationAlreadyExistsError("The selected synonym relation already exists.")

    try:
        relation = build_relation(
            source_word_id=source_word.id,
            target_word_id=target_word.id,
            relation_type=payload.relation_type,
            notes=payload.notes,
        )
        db.add(relation)
        db.flush()

        if payload.relation_type == RelationType.SYNONYM:
            reverse_relation = build_relation(
                source_word_id=target_word.id,
                target_word_id=source_word.id,
                relation_type=payload.relation_type,
                notes=payload.notes,
            )
            db.add(reverse_relation)

        db.commit()
        db.refresh(relation)
        return relation
    except OperationalError as exc:
        db.rollback()
        raise DatabaseConnectionError(
            "Database connection failed while saving word relation."
        ) from exc


def get_word_relations_by_slug(db: Session, slug: str) -> list[WordRelation]:
    try:
        word = db.execute(select(Word).where(Word.slug == slug)).scalar_one_or_none()
    except OperationalError as exc:
        raise DatabaseConnectionError("Database connection failed during slug lookup.") from exc

    if word is None:
        raise WordNotFoundError(f"Word with slug '{slug}' not found.")

    stmt = (
        select(WordRelation)
        .options(selectinload(WordRelation.target_word_ref))
        .where(WordRelation.source_word_id == word.id)
        .order_by(WordRelation.relation_type.asc(), WordRelation.id.asc())
    )

    try:
        return list(db.execute(stmt).scalars().all())
    except OperationalError as exc:
        raise DatabaseConnectionError(
            "Database connection failed while loading word relations."
        ) from exc
