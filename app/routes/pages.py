from fastapi import APIRouter

router = APIRouter(tags=["pages"])


@router.get("/")
def index() -> dict[str, str]:
    return {"message": "Dictionnary FastAPI is running"}
