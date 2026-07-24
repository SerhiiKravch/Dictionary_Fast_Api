# Dictionary Monorepo

Repository layout for the English-Ukrainian dictionary project.

## Structure

```text
backend/   FastAPI API, migrations, tests, Python tooling
frontend/  Reserved for the Next.js application
docs/      Shared project documentation
```

## Backend

The current working application lives in [backend/README.md](./backend/README.md).

Key backend locations:
- `backend/app` - FastAPI application code
- `backend/tests` - unit, API, and integration tests
- `backend/alembic` - database migrations

## Frontend

`frontend/` is intentionally reserved for the upcoming `React + Next.js` application so the repository can evolve as a clean monorepo instead of mixing Python and Node tooling in the root.

## Local Development

Backend from the new layout:

```bash
cd backend
uv run uvicorn app.main:app --reload
```

Docker Compose from the repository root:

```bash
docker compose up --build
```

Test infrastructure from the repository root:

```bash
docker compose -f docker-compose.test.yml up
```
