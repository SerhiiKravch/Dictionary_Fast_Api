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
from app.schemas.word import AutocompleteResponse, WordCreate, WordRead
from app.services.dictionary import autocomplete_words, create_word_manually, list_words

router = APIRouter(prefix="/api", tags=["api"])

DbSession = Annotated[Session, Depends(get_db)]
AutocompleteQuery = Annotated[str, Query(max_length=128)]


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
    response_model=list[WordRead],
    status_code=200,
    responses=COMMON_API_ERROR_RESPONSES,
)
def list_words_endpoint(db: DbSession) -> list[WordRead]:
    words = list_words(db=db)
    return [WordRead.model_validate(word) for word in words]


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
