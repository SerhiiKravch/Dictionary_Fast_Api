# Dictionary FastAPI Backend

FastAPI backend for an English-Ukrainian / Ukrainian-English dictionary with:
- manual word creation
- filtered and paginated dictionary browsing
- autocomplete
- lookup-or-create flow backed by OpenAI

## What This Service Does

The backend stores dictionary entries in PostgreSQL and exposes a JSON API that can be consumed by an external frontend. At the moment the repository is intentionally backend-first: the main product logic, validation, persistence, and OpenAI integration all live here, while `frontend/` in the repo root is reserved for the future Next.js application.

Each saved word currently includes:
- source word
- translation direction
- slug
- transcription
- primary translation
- context sentence
- origin (`manual`, `openai`, `imported`)
- ordered translation options

## Tech Stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2
- Alembic
- PostgreSQL
- Pydantic Settings
- OpenAI Python SDK
- `uv` for dependency management and local workflows
- `pytest` for tests

## Repository Layout

```text
backend/
  app/
    core/         application settings, DB session, error handlers
    exceptions/   domain, DB, and OpenAI exception types
    middleware/   request ID, logging, and middleware setup
    models/       SQLAlchemy models and enums
    routes/       public and /api route modules
    schemas/      request/response DTOs
    services/     dictionary logic and OpenAI integration
    utils/        shared helpers such as slug generation
    main.py       FastAPI app bootstrap
  alembic/        database migrations
  tests/
    api/          API tests against the local test app
    integration/  PostgreSQL-backed integration tests
    unit/         fast isolated tests
  alembic.ini
  Dockerfile
  pyproject.toml
  uv.lock
  .env.example
```

## Prerequisites

- Python 3.12 or newer
- `uv`
- PostgreSQL for local non-Docker development
- an OpenAI API key if you want to use `/lookup` for generated entries

## Environment Configuration

Copy the example file and adjust values for your machine:

```bash
cd backend
cp .env.example .env
```

Main variables:

- `APP_NAME` and `APP_DEBUG`: application metadata and debug mode
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`: local DB defaults
- `DATABASE_URL`: SQLAlchemy connection string
- `OPENAI_API_KEY`: required for generated lookup flow
- `OPENAI_MODEL`: model used by the OpenAI service

The backend currently loads environment variables from `backend/.env`.

## Local Development

Install dependencies and create the project virtual environment:

```bash
cd backend
uv sync
```

Run the API locally:

```bash
cd backend
uv run uvicorn app.main:app --reload
```

Default local URL:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Docker Workflows

From the repository root, run the local app stack:

```bash
docker compose up --build
```

This stack currently starts:
- PostgreSQL
- the FastAPI backend

The backend container mounts `./backend` into `/app`, so code changes are reflected in the container workspace.

For test-only PostgreSQL infrastructure:

```bash
docker compose -f docker-compose.test.yml up
```

## Database Migrations

Apply migrations:

```bash
cd backend
uv run alembic upgrade head
```

Create a new migration:

```bash
cd backend
uv run alembic revision --autogenerate -m "describe_change"
```

Alembic configuration lives in:
- [alembic.ini]
- [alembic/env.py]

## Test Suite

Run the default test suite:

```bash
cd backend
uv run pytest
```

By default, `pytest` excludes integration tests through `pyproject.toml`.

Run only unit tests:

```bash
cd backend
uv run pytest -m unit
```

Run only API tests:

```bash
cd backend
uv run pytest -m api
```

Run integration tests:

```bash
cd backend
uv run pytest -m integration
```

Integration tests require PostgreSQL. You can start the test DB from the repository root:

```bash
docker compose -f docker-compose.test.yml up -d
```

## Linting And Formatting

Run Ruff checks:

```bash
cd backend
uv run ruff check .
```

Format with Ruff:

```bash
cd backend
uv run ruff format .
```

## API Surface

Public JSON routes:
- `GET /`
- `POST /lookup`
- `GET /word/{slug}`

API routes:
- `GET /api/health`
- `GET /api/autocomplete`
- `GET /api/words`
- `GET /api/words/{slug}`
- `POST /api/words`

## Main Application Modules

Important files and responsibilities:

- `app/main.py`: FastAPI app creation and router registration
- `app/core/config.py`: environment-backed settings
- `app/core/db.py`: SQLAlchemy base, engine, session factory, dependency
- `app/routes/public.py`: public JSON endpoints including lookup flow
- `app/routes/api.py`: health, autocomplete, list, detail, and create endpoints
- `app/services/dictionary.py`: main dictionary business logic
- `app/services/openai_service.py`: OpenAI client wrapper and structured generation flow
- `app/models/word.py`: `Word` and `TranslationOption` persistence models
- `app/schemas/word.py`: request and response schemas

## Current Product Shape

Implemented today:
- CRUD-lite flow for reading and creating words
- slug-based detail pages via API
- autocomplete by source-word prefix
- filtered and paginated word listing
- duplicate protection for word direction
- OpenAI-backed lookup-or-create flow
- centralized error handling and typed error responses
- unit, API, and PostgreSQL integration tests

Still intentionally incomplete:
- frontend application in `frontend/`
- authentication and user-specific data
- richer search and ranking
- production-hardened OpenAI prompting and normalization

## Notes For The Planned Frontend

This backend is now structured to support an external Next.js frontend cleanly:
- backend and frontend tooling are separated at the repository level
- no server-rendered template or static-asset layer remains in the backend
- root-level Docker Compose can orchestrate both services later without mixing Python and Node config in one directory
