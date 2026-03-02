Build a minimal full-stack todo app from scratch. 

## What to Build

- **Scope**: Add, complete, and delete todos
- **API**: GET/POST `/todos`, PATCH/DELETE `/todos/{id}`

## Tech Stack

- **Frontend**: Vue 3 (Composition API), Vite, axios. Proxy `/todos` to backend in dev.
- **Backend**: FastAPI, SQLAlchemy, Alembic, SQLite. CORS for localhost:5173.
- **Testing**: Backend pytest + FastAPI TestClient (in-memory SQLite). Frontend Vitest + @vue/test-utils (mock axios).
- **Styling**: CSS that makes the UI polished (typography, spacing, colors, subtle shadows, completed-todo strikethrough). Avoid generic "AI slop" aesthetics.
- **Deployment**: Docker Compose. Caddy serves frontend static files at `/` and reverse-proxies `/api` to the backend. Frontend calls `/api/todos`. Single `docker compose up` to run the full stack.
