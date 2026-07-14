from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.word import WordLookupRequest, WordRead
from app.services.dictionary import get_word_by_slug, lookup_or_create_word

router = APIRouter(tags=["pages"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/")
def index() -> dict[str, str]:
    return {"message": "Dictionary FastAPI is running"}


@router.post("/lookup", response_model=WordRead)
def lookup_word(payload: WordLookupRequest, db: DbSession) -> WordRead:
    word = lookup_or_create_word(db=db, payload=payload)
    return WordRead.model_validate(word)


@router.get("/word/{slug}", response_model=WordRead)
def get_word(slug: str, db: DbSession) -> WordRead:
    word = get_word_by_slug(db=db, slug=slug)
    return WordRead.model_validate(word)
