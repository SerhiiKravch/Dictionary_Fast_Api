from app.schemas.common import ErrorResponse

APPLICATION_ERROR_RESPONSES = {
    500: {"model": ErrorResponse, "description": "Application error"},
}

REQUEST_VALIDATION_ERROR_RESPONSES = {
    422: {"model": ErrorResponse, "description": "Request validation error"},
}

DATABASE_ERROR_RESPONSES = {
    503: {"model": ErrorResponse, "description": "Database unavailable"},
}

DOMAIN_ERROR_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Domain validation error"},
}

NOT_FOUND_ERROR_RESPONSES = {
    404: {"model": ErrorResponse, "description": "Word not found"},
}

CONFLICT_ERROR_RESPONSES = {
    409: {"model": ErrorResponse, "description": "Word already exists"},
}

INTEGRATION_ERROR_RESPONSES = {
    502: {"model": ErrorResponse, "description": "OpenAI integration error"},
}

COMMON_API_ERROR_RESPONSES = {
    **REQUEST_VALIDATION_ERROR_RESPONSES,
    **APPLICATION_ERROR_RESPONSES,
    **DATABASE_ERROR_RESPONSES,
}

COMMON_PAGE_ERROR_RESPONSES = {
    **DOMAIN_ERROR_RESPONSES,
    **NOT_FOUND_ERROR_RESPONSES,
    **REQUEST_VALIDATION_ERROR_RESPONSES,
    **APPLICATION_ERROR_RESPONSES,
    **INTEGRATION_ERROR_RESPONSES,
    **DATABASE_ERROR_RESPONSES,
}
