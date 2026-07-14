from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/health")
def api_health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/autocomplete")
def autocomplete() -> dict[str, list[str]]:
    return {"results": []}
