from app.schemas.common import ErrorResponse


def build_error_response_doc(
    description: str,
    *,
    detail: str,
    error_code: str,
) -> dict[str, object]:
    return {
        "model": ErrorResponse,
        "description": description,
        "content": {
            "application/json": {
                "example": {
                    "detail": detail,
                    "error_code": error_code,
                    "errors": [],
                }
            }
        },
    }


APPLICATION_ERROR_RESPONSES = {
    500: build_error_response_doc(
        "Application error",
        detail="Application error.",
        error_code="application_error",
    ),
}

REQUEST_VALIDATION_ERROR_RESPONSES = {
    422: {
        "model": ErrorResponse,
        "description": "Request validation error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Request validation failed.",
                    "error_code": "request_validation_error",
                    "errors": [
                        {
                            "type": "missing",
                            "loc": ["body", "target_language"],
                            "msg": "Field required",
                            "input": {"source_word": "apple"},
                        }
                    ],
                }
            }
        },
    },
}

DATABASE_ERROR_RESPONSES = {
    503: build_error_response_doc(
        "Database unavailable",
        detail="Database connection is unavailable.",
        error_code="database_connection_error",
    ),
}

DOMAIN_ERROR_RESPONSES = {
    400: build_error_response_doc(
        "Domain validation error",
        detail="Source and target languages must be different.",
        error_code="validation_error",
    ),
}

NOT_FOUND_ERROR_RESPONSES = {
    404: build_error_response_doc(
        "Word not found",
        detail="Word with slug 'cat-en-uk' not found.",
        error_code="word_not_found",
    ),
}

CONFLICT_ERROR_RESPONSES = {
    409: build_error_response_doc(
        "Word already exists",
        detail="Word already exists for the selected translation direction.",
        error_code="word_already_exists",
    ),
}

INTEGRATION_ERROR_RESPONSES = {
    502: build_error_response_doc(
        "OpenAI integration error",
        detail="OpenAI returned an invalid structured response.",
        error_code="openai_response_format_error",
    ),
}

RATE_LIMIT_ERROR_RESPONSES = {
    429: build_error_response_doc(
        "OpenAI rate limit exceeded",
        detail="OpenAI rate limit exceeded.",
        error_code="openai_rate_limit",
    ),
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
    **RATE_LIMIT_ERROR_RESPONSES,
    **INTEGRATION_ERROR_RESPONSES,
    **DATABASE_ERROR_RESPONSES,
}
