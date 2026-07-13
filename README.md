# Dictionary FastAPI

FastAPI-based dictionary service scaffold for an English-Ukrainian / Ukrainian-English dictionary with OpenAI-assisted word generation.

At the current stage, this repository contains the project infrastructure and developer tooling, but the application code itself has not been implemented yet.

## Current Status

The repository is currently at the `project scaffold` stage.

Already prepared:
- Python project initialized with `uv`
- dependencies and dev-dependencies described in `pyproject.toml`
- lockfile committed as `uv.lock`
- `ruff` configured for linting and formatting
- `pre-commit` configured to run checks before commits
- Docker image definition in `Dockerfile`
- local multi-service setup with PostgreSQL in `docker-compose.yml`
- Python version pinned in `.python-version`
- `.gitignore` prepared for Python/uv workflow

Not implemented yet:
- FastAPI application entrypoint
- routes and page handlers
- database models and DB session setup
- Alembic configuration and migrations
- OpenAI integration
- Jinja templates
- static assets
- automated tests
- populated `.env.example`

## Repository Layout

Planned application structure:

```text
app/
  main.py
  config.py
  db.py
  models.py
  schemas.py
  routes/
    pages.py
    api.py
  services/
    dictionary.py
    openai_service.py
  templates/
    base.html
    word_list.html
    word_detail.html
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

Current real state of the repository:

```text
app/                 # empty for now
tests/               # empty for now
Dockerfile
README               # legacy file
README.md            # main project documentation
pyproject.toml
uv.lock
docker-compose.yml
.pre-commit-config.yaml
.python-version
.env.example         # currently empty
.gitignore
```

## Existing Infrastructure

### Dependency and environment management

The project uses `uv` for:
- dependency installation
- lockfile generation
- running local commands
- reproducible environments

Main dependency file:
- `pyproject.toml`

Lockfile:
- `uv.lock`

### Python tooling

Configured developer tooling:
- `ruff` for linting
- `ruff format` for formatting
- `pre-commit` hooks for automatic checks before commit

Current `pre-commit` setup runs:
- `ruff-check --fix`
- `ruff-format`
- end-of-file fix
- trailing whitespace cleanup
- YAML/TOML validation
- merge conflict marker checks

### Containerization

`Dockerfile` is already prepared to:
- use Python 3.12 slim image
- install `uv`
- install project dependencies from `pyproject.toml` and `uv.lock`
- run the app with `uvicorn`

`docker-compose.yml` is already prepared with:
- `db` service using PostgreSQL 16
- `web` service for FastAPI app
- environment variable wiring for `DATABASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL`
- local port mapping `8000:8000`

Important note:
- the container setup expects `app.main:app` to exist, but that file has not been created yet

### Environment configuration

The repository already contains:
- `.python-version` with Python `3.12`
- `.env.example`

Current issue:
- `.env.example` exists but is empty, so it still needs real template variables

Recommended variables for `.env.example`:
- `APP_NAME`
- `APP_ENV`
- `APP_DEBUG`
- `DATABASE_URL`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `OPENAI_TIMEOUT_SECONDS`
- `OPENAI_MAX_RETRIES`

## Planned Product Behavior

Target behavior of the future application:
- show a main page with a list of saved words
- allow selecting translation direction: `en -> uk` or `uk -> en`
- allow entering a word through an HTML form
- if the word already exists in the database, redirect to its detail page
- if the word does not exist, call OpenAI to generate dictionary data
- validate the model response
- save the word and translation options into the database
- show a detail page with transcription, translations, context sentence, and origin
- support autocomplete for existing words

## Recommended Architecture

Suggested responsibilities by module:

- `app/main.py`
  Create FastAPI app, register routers, static files, and template configuration.

- `app/config.py`
  Centralize settings from environment variables using `pydantic-settings`.

- `app/db.py`
  Configure SQLAlchemy engine, session factory, and DB dependency.

- `app/models.py`
  Define `Word` and `TranslationOption` SQLAlchemy models.

- `app/schemas.py`
  Define request/response schemas and validation models.

- `app/routes/pages.py`
  HTML endpoints for main page, lookup flow, and word detail page.

- `app/routes/api.py`
  JSON endpoints such as autocomplete and future health/API routes.

- `app/services/dictionary.py`
  Business logic for normalization, direction parsing, DB lookups, and word creation.

- `app/services/openai_service.py`
  OpenAI client integration, retries, parsing, validation, and response normalization.

## What Should Be Implemented Next

### 1. Create the application skeleton

Create the missing folders and files under `app/`:
- `main.py`
- `config.py`
- `db.py`
- `models.py`
- `schemas.py`
- `routes/pages.py`
- `routes/api.py`
- `services/dictionary.py`
- `services/openai_service.py`
- `templates/`
- `static/`

### 2. Implement settings management

Add environment-driven configuration in `app/config.py`:
- app name and debug mode
- database URL
- OpenAI API key and model
- timeout and retry settings

### 3. Implement database layer

Add SQLAlchemy setup:
- engine
- sessionmaker
- declarative base
- request-scoped DB dependency

Then define models:
- `Word`
- `TranslationOption`

Recommended `Word` fields:
- `id`
- `source_word`
- `source_language`
- `target_language`
- `slug`
- `transcription`
- `primary_translation`
- `context_sentence`
- `origin`
- `created_at`

Recommended `TranslationOption` fields:
- `id`
- `word_id`
- `text`
- `part_of_speech`
- `priority`
- `usage_note`

### 4. Add Alembic migrations

Initialize Alembic and create the first migration for:
- `words` table
- `translation_options` table
- unique constraint for `source_word + source_language + target_language`
- unique slug constraint

### 5. Implement business logic

Move domain logic into `app/services/dictionary.py`:
- normalize user input
- parse direction
- check if word exists
- generate slug
- create `Word` with `TranslationOption[]`
- return autocomplete matches

### 6. Implement OpenAI integration

In `app/services/openai_service.py`:
- call OpenAI Responses API
- request strict JSON output
- validate payload
- normalize parts of speech
- validate context sentence
- deduplicate translation options
- retry on temporary failures

### 7. Implement FastAPI routes

#### HTML routes
- `GET /` for word list page
- `POST /lookup` for processing a submitted word
- `GET /word/{slug}` for word detail page

#### API routes
- `GET /api/autocomplete`
- optional `GET /api/health`

### 8. Add Jinja templates

Create:
- `templates/base.html`
- `templates/word_list.html`
- `templates/word_detail.html`

The templates should support:
- word table
- translation direction form
- error/success messages
- detail page with translation options
- JavaScript autocomplete

### 9. Add tests

Add tests in `tests/` for:
- existing word redirect
- new word creation with mocked OpenAI response
- invalid word handling
- Ukrainian-to-English flow
- autocomplete endpoint
- slug uniqueness
- OpenAI parsing and validation helpers

### 10. Finalize developer experience

Complete project setup by:
- filling `.env.example`
- adding a startup section to the docs once app files exist
- optionally adding `Makefile` or task aliases
- optionally adding CI to run `ruff` and `pytest`

## Suggested Local Workflow

Once the application files are created, the expected workflow will be:

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

Current gaps in the repository:
- no FastAPI code exists yet
- Docker startup will fail until `app.main:app` is implemented
- `.env.example` is empty
- `tests/` is empty
- no Alembic initialization yet
- no CI pipeline yet

## Milestone Plan

### Milestone 1: App bootstrap
- create app files
- create FastAPI instance
- configure settings
- connect templates and static files

### Milestone 2: Database and models
- configure SQLAlchemy
- define models
- create Alembic migrations
- connect PostgreSQL

### Milestone 3: Core dictionary flow
- implement lookup form flow
- redirect on existing word
- create detail page
- add autocomplete

### Milestone 4: OpenAI generation
- integrate OpenAI service
- validate structured output
- save generated words and options
- handle retries and user-facing errors

### Milestone 5: Quality and delivery
- complete tests
- polish templates
- add CI
- verify Docker workflow

## Summary

This repository already has a solid infrastructure base for a FastAPI service:
- dependency management with `uv`
- linting/formatting with `ruff`
- pre-commit hooks
- Docker setup
- PostgreSQL service definition

The next major step is implementing the actual application code under `app/` and `tests/`, starting with the FastAPI entrypoint, settings, DB layer, models, and page routes.
