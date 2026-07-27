import pytest

from app.exceptions.dictionary import InvalidWordRelationError, WordRelationAlreadyExistsError
from app.models.enums import RelationType
from app.services.word_relation_service import create_word_relation, get_word_relations_by_slug
from tests.factories import make_word_create, make_word_relation_create

pytestmark = pytest.mark.unit


def test_create_word_relation_creates_related_link(db_session) -> None:
    from app.services.dictionary import create_word_manually

    first = create_word_manually(db_session, make_word_create(source_word="apple"))
    second = create_word_manually(
        db_session,
        make_word_create(
            source_word="fruit",
            primary_translation="фрукт",
            context_sentence="Fruit is healthy.",
        ),
    )

    relation = create_word_relation(
        db=db_session,
        word_id=first.id,
        payload=make_word_relation_create(
            target_word_id=second.id,
            relation_type=RelationType.RELATED,
        ),
    )

    assert relation.source_word_id == first.id
    assert relation.target_word_id == second.id
    assert relation.relation_type == RelationType.RELATED.value


def test_create_word_relation_rejects_self_relation(db_session) -> None:
    from app.services.dictionary import create_word_manually

    word = create_word_manually(db_session, make_word_create(source_word="apple"))

    with pytest.raises(InvalidWordRelationError):
        create_word_relation(
            db=db_session,
            word_id=word.id,
            payload=make_word_relation_create(target_word_id=word.id),
        )


def test_create_word_relation_rejects_duplicate_relation(db_session) -> None:
    from app.services.dictionary import create_word_manually

    first = create_word_manually(db_session, make_word_create(source_word="apple"))
    second = create_word_manually(
        db_session,
        make_word_create(
            source_word="fruit",
            primary_translation="фрукт",
            context_sentence="Fruit is healthy.",
        ),
    )

    payload = make_word_relation_create(
        target_word_id=second.id,
        relation_type=RelationType.RELATED,
    )
    create_word_relation(db=db_session, word_id=first.id, payload=payload)

    with pytest.raises(WordRelationAlreadyExistsError):
        create_word_relation(db=db_session, word_id=first.id, payload=payload)


def test_create_word_relation_creates_reverse_synonym(db_session) -> None:
    from app.services.dictionary import create_word_manually

    first = create_word_manually(db_session, make_word_create(source_word="big"))
    second = create_word_manually(
        db_session,
        make_word_create(
            source_word="large",
            primary_translation="великий",
            context_sentence="A large house.",
        ),
    )

    create_word_relation(
        db=db_session,
        word_id=first.id,
        payload=make_word_relation_create(
            target_word_id=second.id,
            relation_type=RelationType.SYNONYM,
        ),
    )

    first_relations = get_word_relations_by_slug(db_session, first.slug)
    second_relations = get_word_relations_by_slug(db_session, second.slug)

    assert len(first_relations) == 1
    assert len(second_relations) == 1
    assert first_relations[0].target_word_id == second.id
    assert second_relations[0].target_word_id == first.id
