from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.word import AutocompleteResponse
from app.services.dictionary import autocomplete_words

router = APIRouter(prefix="/api", tags=["api"])

DbSession = Annotated[Session, Depends(get_db)]
AutocompleteQuery = Annotated[str, Query(min_length=1, max_length=128)]


@router.get("/health")
def api_health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/autocomplete", response_model=AutocompleteResponse)
def autocomplete(
    db: DbSession,
    q: AutocompleteQuery = "",
) -> AutocompleteResponse:
    results = autocomplete_words(db=db, query=q)
    return AutocompleteResponse(results=results)
