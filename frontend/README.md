# Frontend

Next.js frontend scaffold for the dictionary project.

This package is intentionally initialized with infrastructure first:

- App Router baseline
- TypeScript configuration
- ESLint setup
- Docker support
- shared folder structure for future features

## Stack

- Next.js
- React
- TypeScript
- ESLint

## Structure

```text
frontend/
  app/          Next.js App Router entrypoints
  components/   reusable UI components
  features/     feature-level modules
  hooks/        custom React hooks
  lib/          env helpers and shared utilities
  public/       static assets
  services/     API client layer
  types/        shared TypeScript types
```

## Environment

Copy the example file before local development:

```bash
cd frontend
cp .env.example .env.local
```

Main variables:

- `NEXT_PUBLIC_API_URL` - public FastAPI base URL for browser requests
- `INTERNAL_API_URL` - optional server-side base URL override for Next.js server runtime

## Local Development

Install dependencies:

```bash
cd frontend
npm install
```

Run the development server:

```bash
cd frontend
npm run dev
```

Default local URL:

```text
http://127.0.0.1:3000
```

## Quality Checks

```bash
cd frontend
npm run lint
npm run typecheck
npm run build
npm run test
```

`npm run test` is currently a placeholder so the frontend package already exposes a stable testing entrypoint before a real test runner is introduced.

## Git Hooks

Frontend checks are enforced through the repository root `pre-commit` configuration.

- `npm --prefix frontend run lint`
- `npm --prefix frontend run typecheck`

`lint-staged` is intentionally not added at this stage to keep the monorepo hook setup centralized in one place.

## Docker

Run the frontend with Docker Compose from the repository root:

```bash
docker compose up --build frontend
```
