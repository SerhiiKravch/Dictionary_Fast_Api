# Dictionary FastAPI

FastAPI-based English-Ukrainian / Ukrainian-English dictionary service with planned OpenAI-assisted word generation.

The repository is no longer just an empty scaffold: it already contains the Python project setup, package layout, initial SQLAlchemy models, and initial Pydantic schemas. The application is still in an early bootstrap stage, so the next focus is wiring configuration, database access, and a runnable FastAPI app.

## Current Status

Implemented now:
- Python project initialized with `uv`
- dependencies and dev-dependencies defined in `pyproject.toml`
- lockfile committed as `uv.lock`
- `ruff` configured for linting and formatting
- `pre-commit` configured for local checks
- Docker image definition in `Dockerfile`
- local `docker-compose.yml` with PostgreSQL
- package-based `app/` layout
- initial SQLAlchemy models for `Word` and `TranslationOption`
- initial Pydantic schemas for lookup and generated payload validation

Still missing:
- working `FastAPI` application entrypoint
- environment-driven settings in `app/config.py`
- SQLAlchemy engine/session setup in `app/db.py`
- Alembic configuration and migrations
- page/API route implementation
- OpenAI service implementation
- templates and static assets
- automated tests
- populated `.env.example`

## Repository Layout

Current repository state:

```text
app/
  __init__.py
  main.py
  config.py
  db.py
  models/
    __init__.py
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

### Models

[`app/models/word.py`](/Users/sergiykravchyshyn/Dev/Dictionary_Fast_Api/app/models/word.py) currently defines:
- `Base`
- `LanguageCode`
- `PartOfSpeech`
- `Word`
- `TranslationOption`

The models already include:
- unique word-per-direction constraint
- unique slug constraint
- one-to-many relationship from `Word` to `TranslationOption`
- timestamps and ordering basics

### Schemas

[`app/schemas/word.py`](/Users/sergiykravchyshyn/Dev/Dictionary_Fast_Api/app/schemas/word.py) currently defines:
- `WordLookupRequest`
- `AutocompleteItem`
- `AutocompleteResponse`
- `GeneratedTranslationOption`
- `GeneratedWordPayload`

These schemas already cover:
- input validation for word lookup
- validation of generated translation options
- validation of a generated dictionary payload before DB save

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
- the container layout is prepared, but the app is not runnable yet because `app/main.py`, `app/config.py`, `app/db.py`, and route modules are still not implemented

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

## Recommended Module Responsibilities

- `app/main.py`
  Create the FastAPI app, register routers, and expose health/docs endpoints.

- `app/config.py`
  Centralize settings from environment variables via `pydantic-settings`.

- `app/db.py`
  Configure SQLAlchemy engine, session factory, and request-scoped DB dependency.

- `app/models/word.py`
  Define ORM enums and models for dictionary storage.

- `app/schemas/word.py`
  Define request/response schemas and generated payload validation.

- `app/routes/pages.py`
  HTML endpoints for the lookup flow and detail pages.

- `app/routes/api.py`
  JSON endpoints such as autocomplete and health/API routes.

- `app/services/dictionary.py`
  Business logic for normalization, direction parsing, lookups, and persistence.

- `app/services/openai_service.py`
  OpenAI integration, retries, parsing, validation, and response normalization.

## What Should Be Implemented Next

### 1. Make the app runnable

Implement:
- `app/config.py`
- `app/db.py`
- `app/main.py`

Minimum expected result:
- `FastAPI()` app exists
- `/health` route works
- `uv run uvicorn app.main:app --reload` starts successfully

### 2. Add DB wiring

Implement in `app/db.py`:
- `create_engine(...)`
- `sessionmaker(...)`
- `get_db()` dependency

### 3. Add environment settings

Implement in `app/config.py`:
- `APP_NAME`
- `APP_DEBUG`
- `DATABASE_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`

### 4. Add Alembic

Create migrations for:
- `words`
- `translation_options`
- unique constraints already described in the models

### 5. Implement minimal routes

Add:
- `GET /health`
- `GET /api/health`
- placeholder lookup/autocomplete routes

### 6. Implement OpenAI and dictionary flow

Once the app and DB are wired:
- implement `app/services/openai_service.py`
- implement `app/services/dictionary.py`
- connect lookup flow to generation and persistence

### 7. Add tests

Start with:
- app startup smoke test
- schema validation tests
- model import / DB session tests

## Suggested Local Workflow

```bash
cp .env.example .env
uv sync --dev
uv run pre-commit install
uv run ruff check .
uv run pytest
uv run uvicorn app.main:app --reload
```

For Docker-based development:

```bash
docker compose up --build
```

## Current Gaps / Risks

- `README.md` previously described the project as a fully empty scaffold; that is no longer true
- `app/main.py`, `app/config.py`, `app/db.py`, `app/routes/api.py`, and `app/routes/pages.py` are still effectively placeholders
- `.env.example` still needs real values
- there is no Alembic setup yet
- there are no tests yet
- Docker startup is not verified end-to-end at the current stage

## Suggested Commit Name

`docs: update README for current project structure and bootstrap status`
