# Frontend

Next.js frontend for the dictionary project with a search-first UX, typed FastAPI integration,
shared UI primitives, route-level fallbacks, and frontend test coverage.

## Stack

- Next.js
- React
- TypeScript
- ESLint
- Vitest
- Testing Library
- Zod

## Structure

```text
frontend/
  app/          App Router routes, layouts, loading and error states
  components/   shared UI primitives
  features/     feature-level modules and tests
  hooks/        custom React hooks
  lib/          env helpers and shared utilities
  public/       static assets
  services/     API client layer and service tests
  test/         shared frontend test setup
  types/        TypeScript types and Zod schemas
```

## Route Map

- `/` search-first home with autocomplete and dictionary lookup
- `/words` catalog with URL-driven filters, pagination, and inline states
- `/words/[slug]` detail page with metadata, translation options, and fallback states
- `/words/new` manual creation flow with client-side validation and submit handling

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

## API Contract Layer

Frontend requests are centralized in `services/api-client.ts`.

- successful API responses are validated with Zod schemas
- backend errors are normalized by `error_code`
- typed dictionary services live in `services/words.ts`

This keeps fetch logic out of UI components and makes frontend/backend contract drift easier to
catch during development.

## UX Coverage

The current frontend includes:

- shared UI primitives for buttons, inputs, cards, fields, badges, and state panels
- route-level `loading.tsx`, `error.tsx`, and `not-found.tsx` coverage for key routes
- inline empty, error, and validation states for catalog, details, search, and manual create flows
- keyboard-aware autocomplete and URL-driven catalog filters

## Quality Checks

```bash
cd frontend
npm run lint
npm run typecheck
npm run build
npm run test
```

Current test coverage includes:

- API client contract handling
- dictionary service calls
- search form and autocomplete interactions
- create word form validation and submit flows
- catalog filters and pagination
- word detail rendering states

## Git Hooks

Frontend checks are enforced through the repository root `pre-commit` configuration.

- `npm --prefix frontend run lint`
- `npm --prefix frontend run typecheck`
- `npm --prefix frontend run test`

`lint-staged` is intentionally not added at this stage to keep the monorepo hook setup centralized in one place.

## Docker

Run the frontend with Docker Compose from the repository root:

```bash
docker compose up --build frontend
```

The current Dockerfile is development-oriented and runs the Next.js dev server inside the compose
setup.
