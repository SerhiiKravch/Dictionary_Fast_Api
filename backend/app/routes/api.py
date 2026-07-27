from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.enums import LanguageCode, WordOrigin
from app.routes.responses import (
    APPLICATION_ERROR_RESPONSES,
    COMMON_API_ERROR_RESPONSES,
    CONFLICT_ERROR_RESPONSES,
    DOMAIN_ERROR_RESPONSES,
    NOT_FOUND_ERROR_RESPONSES,
    RELATION_CONFLICT_ERROR_RESPONSES,
)
from app.schemas.common import HealthResponse
from app.schemas.word import (
    AutocompleteResponse,
    WordCreate,
    WordListResponse,
    WordRead,
    WordRelationCreate,
    WordRelationListResponse,
    WordRelationRead,
)
from app.services.dictionary import (
    autocomplete_words,
    create_word_manually,
    get_word_by_slug,
    paginate_words,
)
from app.services.word_relation_service import create_word_relation, get_word_relations_by_slug

router = APIRouter(prefix="/api", tags=["api"])

DbSession = Annotated[Session, Depends(get_db)]
AutocompleteQuery = Annotated[str, Query(max_length=128)]
PaginationLimit = Annotated[int, Query(ge=1, le=100)]
PaginationOffset = Annotated[int, Query(ge=0)]
WordSearchQuery = Annotated[str, Query(max_length=128)]


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=200,
    responses=APPLICATION_ERROR_RESPONSES,
)
def api_health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get(
    "/autocomplete",
    response_model=AutocompleteResponse,
    status_code=200,
    responses=COMMON_API_ERROR_RESPONSES,
)
def autocomplete_endpoint(
    db: DbSession,
    q: AutocompleteQuery = "",
) -> AutocompleteResponse:
    results = autocomplete_words(db=db, query=q)
    return AutocompleteResponse(results=results)


@router.get(
    "/words",
    response_model=WordListResponse,
    status_code=200,
    responses=COMMON_API_ERROR_RESPONSES,
)
def list_words_endpoint(
    db: DbSession,
    limit: PaginationLimit = 20,
    offset: PaginationOffset = 0,
    source_language: LanguageCode | None = None,
    target_language: LanguageCode | None = None,
    origin: WordOrigin | None = None,
    search: WordSearchQuery = "",
) -> WordListResponse:
    items, total = paginate_words(
        db=db,
        limit=limit,
        offset=offset,
        source_language=source_language,
        target_language=target_language,
        origin=origin,
        search=search,
    )
    return WordListResponse(
        items=[WordRead.model_validate(word) for word in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/words/{slug}",
    response_model=WordRead,
    status_code=200,
    responses={
        **COMMON_API_ERROR_RESPONSES,
        **NOT_FOUND_ERROR_RESPONSES,
    },
)
def get_word_endpoint(
    slug: str,
    db: DbSession,
) -> WordRead:
    word = get_word_by_slug(db=db, slug=slug)
    return WordRead.model_validate(word)


@router.post(
    "/words",
    response_model=WordRead,
    status_code=201,
    responses={
        **COMMON_API_ERROR_RESPONSES,
        **DOMAIN_ERROR_RESPONSES,
        **CONFLICT_ERROR_RESPONSES,
    },
)
def create_word_endpoint(
    payload: WordCreate,
    db: DbSession,
) -> WordRead:
    word = create_word_manually(db=db, payload=payload)
    return WordRead.model_validate(word)


@router.post(
    "/words/{word_id}/relations",
    response_model=WordRelationRead,
    status_code=201,
    responses={
        **COMMON_API_ERROR_RESPONSES,
        **DOMAIN_ERROR_RESPONSES,
        **NOT_FOUND_ERROR_RESPONSES,
        **RELATION_CONFLICT_ERROR_RESPONSES,
    },
)
def create_word_relation_endpoint(
    word_id: int,
    payload: WordRelationCreate,
    db: DbSession,
) -> WordRelationRead:
    relation = create_word_relation(db=db, word_id=word_id, payload=payload)
    return WordRelationRead(
        id=relation.id,
        relation_type=relation.relation_type,
        notes=relation.notes,
        related_word=relation.target_word_ref,
    )


@router.get(
    "/words/{slug}/relations",
    response_model=WordRelationListResponse,
    status_code=200,
    responses={
        **COMMON_API_ERROR_RESPONSES,
        **NOT_FOUND_ERROR_RESPONSES,
    },
)
def list_word_relations_endpoint(
    slug: str,
    db: DbSession,
) -> WordRelationListResponse:
    relations = get_word_relations_by_slug(db=db, slug=slug)
    return WordRelationListResponse(
        items=[
            WordRelationRead(
                id=relation.id,
                relation_type=relation.relation_type,
                notes=relation.notes,
                related_word=relation.target_word_ref,
            )
            for relation in relations
        ]
    )
