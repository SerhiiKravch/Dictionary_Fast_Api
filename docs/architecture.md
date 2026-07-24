# Architecture Notes

## Repository Strategy

The project now follows a lightweight monorepo structure:

- `backend/` contains the FastAPI service and all Python-related tooling.
- `frontend/` contains a separate Next.js application scaffold.
- repository root is used only for shared orchestration and documentation.

## Why This Split

- avoids collisions between Python's `app/` package and Next.js `app/` routing
- keeps `pyproject.toml` and future `package.json` isolated
- lets Docker Compose orchestrate both services from the root
- makes CI easier to split into backend and frontend pipelines later
- keeps frontend dependencies, linting, and runtime config local to the UI package
