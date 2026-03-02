---
auto-captured: true
tags: [architecture, full-stack, docker]
scope: project
summary: Full-stack todo app with Vue 3 + FastAPI, Caddy reverse proxy, Docker Compose
---

# Architecture

## What

Monorepo with separate backend (FastAPI) and frontend (Vue 3) apps. Caddy serves as single entry point: static frontend at `/`, API at `/api` reverse-proxied to backend. Single `docker compose up` runs the full stack.

## When to Use

- Adding new API routes or frontend features
- Configuring deployment or dev proxy

## Key Components

- **Backend**: `backend/` — FastAPI, SQLAlchemy, Alembic, SQLite. Runs on port 8000 internally.
- **Frontend**: `frontend/` — Vue 3 Composition API, Vite, axios. Built with `VITE_API_BASE=/api` for production.
- **Caddy**: `Caddyfile` — `handle_path /api/*` strips `/api` and proxies to backend; `handle` serves frontend.
- **Dev**: Vite proxy `/todos` → `http://localhost:8000/todos`; frontend uses empty base URL.

## API Paths

- Dev: frontend calls `/todos` (proxied)
- Prod: frontend calls `/api/todos` (Caddy → backend `/todos`)

## Related

- `patterns/backend-api.md`
- `patterns/frontend-api.md`
