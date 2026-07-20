from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.routes.responses import (
    APPLICATION_ERROR_RESPONSES,
    COMMON_API_ERROR_RESPONSES,
    CONFLICT_ERROR_RESPONSES,
    DOMAIN_ERROR_RESPONSES,
)
from app.schemas.common import HealthResponse
from app.schemas.word import AutocompleteResponse, WordCreate, WordListResponse, WordRead
from app.services.dictionary import autocomplete_words, create_word_manually, paginate_words

router = APIRouter(prefix="/api", tags=["api"])

DbSession = Annotated[Session, Depends(get_db)]
AutocompleteQuery = Annotated[str, Query(max_length=128)]
PaginationLimit = Annotated[int, Query(ge=1, le=100)]
PaginationOffset = Annotated[int, Query(ge=0)]


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
) -> WordListResponse:
    items, total = paginate_words(db=db, limit=limit, offset=offset)
    return WordListResponse(
        items=[WordRead.model_validate(word) for word in items],
        total=total,
        limit=limit,
        offset=offset,
    )


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
