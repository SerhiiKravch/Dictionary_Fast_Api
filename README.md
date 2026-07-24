# Dictionary Monorepo

Repository layout for the English-Ukrainian dictionary project.

## Structure

```text
backend/   FastAPI API, migrations, tests, Python tooling
frontend/  Next.js frontend scaffold and future UI application
docs/      Shared project documentation
```

## Backend

The current working application lives in [backend/README.md](./backend/README.md).

Key backend locations:
- `backend/app` - FastAPI application code
- `backend/tests` - unit, API, and integration tests
- `backend/alembic` - database migrations

## Frontend

`frontend/` now contains the initialized `React + Next.js` scaffold so the repository can evolve as a clean monorepo without mixing Python and Node tooling in the root.

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

Frontend only:

```bash
cd frontend
npm install
npm run dev
```

Test infrastructure from the repository root:

```bash
docker compose -f docker-compose.test.yml up
```
