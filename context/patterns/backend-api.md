---
auto-captured: true
tags: [pattern, backend, api, fastapi]
scope: backend
summary: FastAPI CRUD with SQLAlchemy, Pydantic schemas, TestClient + in-memory SQLite
---

# Backend API Pattern

## What

REST endpoints with FastAPI routers, SQLAlchemy ORM, Pydantic request/response schemas. Tests use FastAPI TestClient with in-memory SQLite (`StaticPool`) for isolation.

## Implementation

```python
# backend/app/routers/todos.py
router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("", response_model=list[TodoResponse])
def list_todos(session: Session = Depends(get_session)):
    return session.query(Todo).all()

@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(body: TodoCreate, session: Session = Depends(get_session)):
    todo = Todo(**body.model_dump())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return TodoResponse.model_validate(todo)
```

## Key Decisions

- `get_session` context manager for DB; convert to Pydantic inside session to avoid DetachedInstanceError.
- `conftest.py` sets `DATABASE_URL=sqlite:///:memory:` before imports; `_create_tables` uses `Base.metadata.create_all()`.
- Schema validation: `TodoCreate.title` uses `Field(..., min_length=1)` for empty-title rejection.
