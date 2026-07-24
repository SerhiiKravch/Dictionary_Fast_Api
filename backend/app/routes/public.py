from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.routes.responses import (
    APPLICATION_ERROR_RESPONSES,
    COMMON_PAGE_ERROR_RESPONSES,
    CONFLICT_ERROR_RESPONSES,
)
from app.schemas.common import MessageResponse
from app.schemas.word import WordLookupRequest, WordRead
from app.services.dictionary import get_word_by_slug, lookup_or_create_word

router = APIRouter(tags=["public"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get(
    "/",
    response_model=MessageResponse,
    status_code=200,
    responses=APPLICATION_ERROR_RESPONSES,
)
def index_endpoint() -> MessageResponse:
    return MessageResponse(message="Dictionary FastAPI is running")


@router.post(
    "/lookup",
    response_model=WordRead,
    status_code=200,
    responses={
        **COMMON_PAGE_ERROR_RESPONSES,
        **CONFLICT_ERROR_RESPONSES,
    },
)
def lookup_word_endpoint(payload: WordLookupRequest, db: DbSession) -> WordRead:
    word = lookup_or_create_word(db=db, payload=payload)
    return WordRead.model_validate(word)


@router.get(
    "/word/{slug}",
    response_model=WordRead,
    status_code=200,
    responses=COMMON_PAGE_ERROR_RESPONSES,
)
def get_word_endpoint(slug: str, db: DbSession) -> WordRead:
    word = get_word_by_slug(db=db, slug=slug)
    return WordRead.model_validate(word)
