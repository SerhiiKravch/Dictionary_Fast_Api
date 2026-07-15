from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.common import ErrorResponse, HealthResponse
from app.schemas.word import AutocompleteResponse, WordCreate, WordRead
from app.services.dictionary import autocomplete_words, create_word_manually, list_words

router = APIRouter(prefix="/api", tags=["api"])

DbSession = Annotated[Session, Depends(get_db)]
AutocompleteQuery = Annotated[str, Query(min_length=1, max_length=128)]

COMMON_ERROR_RESPONSES = {
    422: {"model": ErrorResponse, "description": "Request validation error"},
    500: {"model": ErrorResponse, "description": "Application error"},
    503: {"model": ErrorResponse, "description": "Database unavailable"},
}


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=200,
    responses={500: {"model": ErrorResponse, "description": "Application error"}},
)
def api_health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get(
    "/autocomplete",
    response_model=AutocompleteResponse,
    status_code=200,
    responses=COMMON_ERROR_RESPONSES,
)
def autocomplete_endpoint(
    db: DbSession,
    q: AutocompleteQuery = "",
) -> AutocompleteResponse:
    results = autocomplete_words(db=db, query=q)
    return AutocompleteResponse(results=results)


@router.get(
    "/words",
    response_model=list[WordRead],
    status_code=200,
    responses=COMMON_ERROR_RESPONSES,
)
def list_words_endpoint(db: DbSession) -> list[WordRead]:
    words = list_words(db=db)
    return [WordRead.model_validate(word) for word in words]


@router.post(
    "/words",
    response_model=WordRead,
    status_code=201,
    responses={
        **COMMON_ERROR_RESPONSES,
        400: {"model": ErrorResponse, "description": "Domain validation error"},
        409: {"model": ErrorResponse, "description": "Word already exists"},
    },
)
def create_word_endpoint(
    payload: WordCreate,
    db: DbSession,
) -> WordRead:
    word = create_word_manually(db=db, payload=payload)
    return WordRead.model_validate(word)
