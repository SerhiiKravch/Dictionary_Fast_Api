# Dictionary FastAPI

FastAPI-based English-Ukrainian / Ukrainian-English dictionary service with planned OpenAI-assisted word generation.

The repository is already past the empty-scaffold stage. It now contains:
- project tooling and dependency setup
- package-based application layout
- SQLAlchemy models and Alembic migration setup
- Pydantic schemas
- basic API/page routers
- custom exception hierarchy and FastAPI error handlers
- a service layer for dictionary lookup, manual persistence, pagination, slug generation, and OpenAI integration

The application is still in an early product stage, but the bootstrap infrastructure is already in place.

## Current Status

Implemented now:
- Python project initialized with `uv`
- dependencies and dev-dependencies defined in `pyproject.toml`
- lockfile committed as `uv.lock`
- `ruff` configured for linting and formatting
- `pre-commit` configured for local checks
- Docker image definition in `Dockerfile`
- local `docker-compose.yml` with PostgreSQL
- package-based `app/` layout with `core`, `models`, `schemas`, `routes`, `services`, and `exceptions`
- SQLAlchemy models for `Word` and `TranslationOption`
- Pydantic schemas for lookup, generated payloads, create/read DTOs, paginated list responses, and shared success/error responses
- Alembic configuration with an initial migration for `words` and `translation_options`
- FastAPI application bootstrap in `app/main.py`
- routes for `GET /`, `POST /lookup`, `GET /word/{slug}`, `GET /api/health`, `GET /api/autocomplete`, `GET /api/words`, `GET /api/words/{slug}`, and `POST /api/words`
- custom exception hierarchy, centralized error handlers, and reusable OpenAPI error-response definitions with examples
- service-layer logic for dictionary lookup, manual word creation, filtered/paginated list endpoints, autocomplete, and OpenAI calls
- automated unit and API tests for service logic, lookup flow, pagination, filters, autocomplete, slug helpers, and OpenAI configuration errors
- populated `.env.example`

Still missing or incomplete:
- full HTML page flow and templates
- production-ready OpenAI prompt/response normalization
- end-to-end Docker verification for the full flow

## Repository Layout

Current repository state:

```text
app/
  __init__.py
  main.py
  core/
    __init__.py
    config.py
    db.py
    error_handlers.py
  exceptions/
    __init__.py
    database.py
    dictionary.py
    openai.py
  models/
    __init__.py
    enums.py
    word.py
  schemas/
    __init__.py
    common.py
    word.py
  routes/
    __init__.py
    pages.py
    api.py
  services/
    __init__.py
    dictionary.py
    openai_service.py
  utils/
    __init__.py
    slug.py
alembic/
  env.py
  script.py.mako
  versions/
alembic.ini
tests/
  conftest.py
  factories.py
  fakes.py
  api/
    __init__.py
    test_autocomplete_api.py
    test_health_api.py
    test_words_api.py
  unit/
    __init__.py
    test_dictionary_service.py
    test_lookup_or_create_word.py
    test_openai_service.py
    test_slug_utils.py
  integration/
    conftest.py
    test_postgres_integration.py
Dockerfile
docker-compose.yml
docker-compose.test.yml
pyproject.toml
uv.lock
.pre-commit-config.yaml
.python-version
.env.example
.gitignore
README.md
```

## Existing Code

### Core infrastructure

`app/core/config.py` contains:
- application settings via `pydantic-settings`
- environment loading from `.env`
- database and OpenAI defaults

`app/core/db.py` contains:
- shared SQLAlchemy `Base`
- `engine`
- `SessionLocal`
- `get_db()` dependency

`app/core/error_handlers.py` contains:
- FastAPI exception handler registration
- mapping of domain/integration/persistence exceptions to HTTP responses
- explicit handling for missing or invalid OpenAI configuration
- unified JSON error payloads with `detail`, `error_code`, and `errors`

### Exceptions

`app/exceptions/` currently groups:
- base app exceptions
- dictionary/domain exceptions
- OpenAI integration exceptions
- database/persistence exceptions
- OpenAI configuration exceptions

### Models

`app/models/enums.py` defines:
- `LanguageCode`
- `WordOrigin`
- `PartOfSpeech`

`app/models/word.py` defines:
- `Word`
- `TranslationOption`

The models already include:
- unique word-per-direction constraint
- unique slug constraint
- database-level language-difference check constraint
- database-level origin check constraint
- one-to-many relationship from `Word` to `TranslationOption`
- `created_at` and `updated_at` timestamps
- deterministic translation-option ordering by priority

### Schemas

`app/schemas/word.py` currently defines:
- `WordLookupRequest`
- `AutocompleteItem`
- `AutocompleteResponse`
- `GeneratedTranslationOption`
- `GeneratedWordPayload`
- `TranslationOptionCreate`
- `WordCreate`
- `TranslationOptionRead`
- `WordRead`
- `WordListResponse`

These schemas already cover:
- input validation for word lookup
- validation of generated translation options
- generated dictionary payload validation
- read/create DTOs for persistence and API responses
- paginated API responses for saved-word collections

`app/schemas/common.py` currently defines:
- `HealthResponse`
- `MessageResponse`
- `ErrorResponse`

### Routes

`app/routes/pages.py` currently exposes:
- `GET /`
- `POST /lookup`
- `GET /word/{slug}`

These root-level routes currently return JSON and declare typed error responses in OpenAPI for:
- validation errors
- not found errors
- OpenAI integration errors
- database availability errors

`app/routes/api.py` currently exposes:
- `GET /api/health`
- `GET /api/autocomplete`
- `GET /api/words`
- `GET /api/words/{slug}`
- `POST /api/words`

These API routes now declare typed `ErrorResponse` models in OpenAPI for:
- request validation errors
- domain validation errors
- duplicate-word conflicts
- application/database failures
- rate-limit and integration failures where applicable
- missing OpenAI configuration during lookup flow

Shared OpenAPI error-response maps are now centralized in:
- `app/routes/responses.py`
- these maps also include concrete JSON examples for Swagger / OpenAPI

### Services

`app/services/dictionary.py` currently contains:
- word normalization
- direction parsing
- lookup by direction
- lookup by slug
- slug generation via dedicated utilities
- autocomplete query
- creation of `Word` with `TranslationOption[]`
- filtered and paginated listing of saved words
- orchestration of lookup-or-create flow
- database connectivity error translation into app exceptions
- typed translation option input handling for both manual and generated create flows

`app/services/openai_service.py` currently contains:
- OpenAI client initialization
- explicit API-key/configuration validation
- prompt generation
- structured response parsing
- basic API/rate-limit error translation into app exceptions

`app/utils/slug.py` currently contains:
- source-word slug normalization
- readable base slug generation
- short suffix generation for slug conflicts
- reusable slug helpers shared by service-layer create flows

### Tests

The current test suite covers:
- normalization and direction parsing
- manual word creation
- duplicate-word protection
- slug conflict retry behavior
- lookup-or-create flow with OpenAI mocked out
- API health/list/detail/create/not-found/validation scenarios
- list filtering by language, origin, and search query
- autocomplete behavior, including empty-query handling and result limiting
- reusable slug helper behavior
- OpenAI configuration error behavior
- PostgreSQL integration checks for constraints, filtered API responses, and nested detail loading

Test helpers are organized as:
- `tests/conftest.py` for DB and client fixtures
- `tests/integration/conftest.py` for real PostgreSQL fixtures and Alembic bootstrap
- `tests/factories.py` for reusable payload builders
- `tests/fakes.py` for fake OpenAI service implementations

Tests are grouped by level:
- `tests/unit/` for service, utility, and isolated logic tests
- `tests/api/` for FastAPI endpoint tests on the lightweight SQLite test layer
- `tests/integration/` for real PostgreSQL-backed integration tests

### Database migrations

Alembic is already configured through:
- `alembic.ini`
- `alembic/env.py`

The first migration already exists:
- `alembic/versions/4629186736bf_create_words_and_translation_options.py`

## Tooling

### Dependency management

The project uses `uv` for:
- dependency installation
- lockfile generation
- running local commands
- reproducible virtual environments

### Linting and formatting

Configured tooling:
- `ruff` for linting
- `ruff format` for formatting
- `pre-commit` hooks for local checks

Current `pre-commit` setup runs:
- `ruff-check --fix`
- `ruff-format`
- end-of-file fix
- trailing whitespace cleanup
- YAML/TOML validation
- merge conflict marker checks

### Containerization

The repository already includes:
- `Dockerfile`
- `docker-compose.yml` with PostgreSQL 16
- `docker-compose.test.yml` with a dedicated PostgreSQL 16 instance for integration tests

Important note:
- the infrastructure is prepared, but the user-facing product flow is still incomplete until services, routes, templates, and tests are fully finished

## API Contract

Current JSON API endpoints:
- `GET /api/health`
- `GET /api/autocomplete?q=<prefix>`
- `GET /api/words?limit=<n>&offset=<n>&source_language=<code>&target_language=<code>&origin=<value>&search=<text>`
- `GET /api/words/{slug}`
- `POST /api/words`

Current root-level endpoints:
- `GET /`
- `POST /lookup`
- `GET /word/{slug}`

Successful responses are typed with dedicated Pydantic models.

`GET /api/autocomplete` returns:
- `{"results": []}` for an empty query
- up to 10 matching values for a non-empty prefix

`GET /api/words` returns a paginated envelope:

```json
{
  "items": [],
  "total": 0,
  "limit": 20,
  "offset": 0
}
```

`GET /api/words/{slug}` returns a single `WordRead` object with nested `translation_options`.

Error responses are now standardized as:

```json
{
  "detail": "Word with slug 'cat-en-uk' not found.",
  "error_code": "word_not_found",
  "errors": []
}
```

The `errors` array is mainly used for request validation failures such as malformed JSON bodies or missing required fields.

## Planned Product Behavior

Target application behavior:
- show a main page with a list of saved words
- allow selecting translation direction: `en -> uk` or `uk -> en`
- allow entering a word through an HTML form
- if the word already exists in the database, redirect to its detail page
- if the word does not exist, call OpenAI to generate dictionary data
- validate the model response
- save the word and translation options into the database
- show a detail page with transcription, translations, context sentence, and origin
- support autocomplete for existing words

## Recommended Next Steps

### 1. Stabilize the current service layer

Improve:
- OpenAI response normalization and validation hardening
- richer database error coverage in services beyond `dictionary.py`

### 2. Expand the routes

Add:
- filtering and sorting options for `GET /api/words`
- Swagger `responses` coverage for every future endpoint

Implemented already:
- `GET /api/words/{slug}` JSON detail lookup
- filtering for `source_language`, `target_language`, `origin`, and `search`
- pagination via `limit` and `offset`

### 3. Add templates and page flow

Create:
- `templates/base.html`
- `templates/word_list.html`
- `templates/word_detail.html`

### 4. Add tests

Start with:
- app startup smoke test
- route tests for `/` and page-form behavior
- schema validation tests
- service tests for OpenAI error translation and DB failure branches
- migration smoke test

Already covered:
- service tests for normalization, duplicate protection, slug retries, and lookup-or-create flow
- API tests for list pagination, filters, autocomplete, detail lookup, create, and validation errors
- utility tests for slug generation helpers
- OpenAI configuration error test

### 5. Verify database and Docker flow

Validate:
- `uv run alembic upgrade head`
- `docker compose up -d db`
- end-to-end DB connectivity and migration flow

## Suggested Local Workflow

```bash
cp .env.example .env
uv sync --dev
uv run pre-commit install
uv run ruff check .
uv run pytest
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

For Docker-based development:

```bash
docker compose up --build
```

For PostgreSQL integration tests:

```bash
docker compose -f docker-compose.test.yml up -d db_test
DATABASE_URL_TEST=postgresql+psycopg://dictionary_user:dictionary_pass@localhost:5434/dictionary_test \
uv run pytest -m integration
```

Notes:
- regular `pytest` excludes integration tests by default
- integration tests run Alembic migrations against the test database before executing

## Current Gaps / Risks

- the service layer still needs hardening around race conditions and persistence conflicts
- OpenAI integration still needs production-ready retry/validation behavior
- root-level routes still return JSON, so HTML templates and user-facing page flow are not implemented yet
- full Docker end-to-end verification is still pending
