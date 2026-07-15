from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.common import ErrorResponse, MessageResponse
from app.schemas.word import WordLookupRequest, WordRead
from app.services.dictionary import get_word_by_slug, lookup_or_create_word

router = APIRouter(tags=["pages"])

DbSession = Annotated[Session, Depends(get_db)]

PAGE_ERROR_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Domain validation error"},
    404: {"model": ErrorResponse, "description": "Word not found"},
    422: {"model": ErrorResponse, "description": "Request validation error"},
    500: {"model": ErrorResponse, "description": "Application error"},
    502: {"model": ErrorResponse, "description": "OpenAI integration error"},
    503: {"model": ErrorResponse, "description": "Database unavailable"},
}


@router.get(
    "/",
    response_model=MessageResponse,
    status_code=200,
    responses={500: {"model": ErrorResponse, "description": "Application error"}},
)
def index_page() -> MessageResponse:
    return MessageResponse(message="Dictionary FastAPI is running")


@router.post(
    "/lookup",
    response_model=WordRead,
    status_code=200,
    responses={
        **PAGE_ERROR_RESPONSES,
        409: {"model": ErrorResponse, "description": "Word already exists"},
    },
)
def lookup_word_page(payload: WordLookupRequest, db: DbSession) -> WordRead:
    word = lookup_or_create_word(db=db, payload=payload)
    return WordRead.model_validate(word)


@router.get(
    "/word/{slug}",
    response_model=WordRead,
    status_code=200,
    responses=PAGE_ERROR_RESPONSES,
)
def get_word_page(slug: str, db: DbSession) -> WordRead:
    word = get_word_by_slug(db=db, slug=slug)
    return WordRead.model_validate(word)
