# Dictionary FastAPI

FastAPI-based English-Ukrainian / Ukrainian-English dictionary service with planned OpenAI-assisted word generation.

The repository is already past the empty-scaffold stage. It now contains:
- project tooling and dependency setup
- package-based application layout
- SQLAlchemy models and Alembic migration setup
- Pydantic schemas
- basic API/page routers
- custom exception hierarchy and FastAPI error handlers
- an initial service layer for dictionary lookup and OpenAI integration

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
- Pydantic schemas for lookup, generated payloads, create/read DTOs, and autocomplete responses
- Alembic configuration with an initial migration for `words` and `translation_options`
- FastAPI application bootstrap in `app/main.py`
- basic routes for `/`, `/health`, `/api/health`, `/api/autocomplete`, `/lookup`, and `/word/{slug}`
- custom exception hierarchy and centralized error handlers
- initial service-layer structure for dictionary lookup and OpenAI calls
- populated `.env.example`

Still missing or incomplete:
- full HTML page flow and templates
- production-ready OpenAI prompt/response normalization
- robust retry and fallback logic around slug generation and persistence
- manual word creation route without OpenAI
- automated tests
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
    word.py
  routes/
    __init__.py
    pages.py
    api.py
  services/
    __init__.py
    dictionary.py
    openai_service.py
  templates/
  static/
alembic/
  env.py
  script.py.mako
  versions/
alembic.ini
tests/
Dockerfile
docker-compose.yml
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

### Exceptions

`app/exceptions/` currently groups:
- base app exceptions
- dictionary/domain exceptions
- OpenAI integration exceptions
- database/persistence exceptions

### Models

`app/models/enums.py` defines:
- `LanguageCode`
- `PartOfSpeech`

`app/models/word.py` defines:
- `Word`
- `TranslationOption`

The models already include:
- unique word-per-direction constraint
- unique slug constraint
- one-to-many relationship from `Word` to `TranslationOption`
- timestamps and ordering basics

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

These schemas already cover:
- input validation for word lookup
- validation of generated translation options
- generated dictionary payload validation
- read/create DTOs for persistence and API responses

### Routes

`app/routes/pages.py` currently exposes:
- `GET /`
- `POST /lookup`
- `GET /word/{slug}`

`app/routes/api.py` currently exposes:
- `GET /api/health`
- `GET /api/autocomplete`

### Services

`app/services/dictionary.py` currently contains:
- word normalization
- direction parsing
- lookup by direction
- lookup by slug
- slug generation
- autocomplete query
- creation of `Word` with `TranslationOption[]`
- orchestration of lookup-or-create flow

`app/services/openai_service.py` currently contains:
- OpenAI client initialization
- prompt generation
- structured response parsing
- basic API/rate-limit error translation into app exceptions

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

Important note:
- the infrastructure is prepared, but the user-facing product flow is still incomplete until services, routes, templates, and tests are fully finished

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
- retry and fallback logic around slug creation and `IntegrityError`
- OpenAI response normalization and validation hardening
- manual word creation flow without OpenAI

### 2. Expand the routes

Add:
- `POST /api/words` for manual word creation
- richer lookup response behavior
- proper error mapping for all domain cases

### 3. Add templates and page flow

Create:
- `templates/base.html`
- `templates/word_list.html`
- `templates/word_detail.html`

### 4. Add tests

Start with:
- app startup smoke test
- route tests for `/`, `/health`, `/api/health`, `/api/autocomplete`
- schema validation tests
- dictionary service unit tests
- migration smoke test

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

## Current Gaps / Risks

- the service layer still needs hardening around race conditions and persistence conflicts
- OpenAI integration still needs production-ready retry/validation behavior
- there are no automated tests yet
- HTML templates and user-facing page flow are not implemented
- manual word creation flow without OpenAI is not implemented yet
- full Docker end-to-end verification is still pending
