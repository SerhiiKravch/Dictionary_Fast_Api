from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str
    error_code: str
    errors: list[dict[str, object]] = Field(default_factory=list)
